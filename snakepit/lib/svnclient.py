import weakref
import posixpath
import os.path
from datetime import datetime

application_pool = None

def _import_svn():
    global fs, repos, core, delta,_kindmap
    from svn import fs, repos, core, delta
    _kindmap = {
        core.svn_node_dir: 'D',
        core.svn_node_file: 'F'
        }
    Pool.apr_pool_clear = staticmethod(core.apr_pool_clear)
    Pool.apr_terminate = staticmethod(core.apr_terminate)
    Pool.apr_pool_destroy = staticmethod(core.apr_pool_destroy)
    
def to_unicode(string, encoding):
    return string

def _to_svn(*args):
    return '/'.join([p for p in [p.strip('/') for p in args] if p]) \
           .encode('utf-8')

def _from_svn(path):
    return path and to_unicode(path, 'utf-8')

def _normalize_path(path):
    """Remove leading "/", except for the root."""
    return path and path.strip('/') or '/'

def _path_within_scope(scope, fullpath):
    """Remove the leading scope from repository paths.
    
    Return `None` if the path is not in scope.
    """
    if fullpath is not None:
        fullpath = fullpath.lstrip('/')
        if scope == '/':
            return _normalize_path(fullpath)
        scope = scope.strip('/')
        if (fullpath + '/').startswith(scope + '/'):
            return fullpath[len(scope) + 1:] or '/'

def _is_path_within_scope(scope, fullpath):
    """Check whether the given `fullpath` is within the given `scope`"""
    if scope == '/':
        return fullpath is not None
    fullpath = fullpath and fullpath.lstrip('/') or ''
    scope = scope.strip('/')
    return (fullpath + '/').startswith(scope + '/')
    
def _svn_rev(number):
    value = core.svn_opt_revision_value_t()
    value.number = number
    revision = core.svn_opt_revision_t()
    revision.kind = core.svn_opt_revision_number
    revision.value = value
    return revision

def _svn_head():
    revision = core.svn_opt_revision_t()
    revision.kind = core.svn_opt_revision_head
    return revision

def _mark_weakpool_invalid(weakpool):
    if weakpool():
        weakpool()._mark_invalid()
    
class Pool(object):
    """ A pythonic memory pool object"""
    
    def __init__(self, parent_pool=None):
        global application_pool
        self._parent_pool = parent_pool or application_pool
        
        if self._parent_pool:
            self._pool = core.svn_pool_create(self._parent_pool())
        else:
            core.apr_initialize()
            application_pool = self
            
            self._pool = core.svn_pool_create(None)
        self._mark_valid()
    
    def __call__(self):
        return self._pool
    
    def valid(self):
        """Check whether this memory pool and its parents are still valid"""
        return hasattr(self, '_is_valid')
    
    def assert_valid(self):
        """Assert that this memory_pool is still valid."""
        assert self.valid()
    
    def clear(self):
        """Clear embedded memory pool. Invalidate all subpools"""
        self.apr_pool_clear(self._pool)
        self._mark_valid()
        
    def destroy(self):
        """Destroy embedded memory pool. If you do not destroy the memory
        pool manually, Python will destroy it automatically"""
        
        global application_pool
        
        self.assert_valid()
        
        self.apr_pool_destroy(self._pool)
        
        if not self._parent_pool:
            application_pool = None
            self.apr_terminate()
        
        self._mark_invalid()
    
    def __del__(self):
        """Automatically destroy memory pools, if necessary"""
        if self.valid():
            self.destroy()
    
    def _mark_valid(self):
        """Mark pool as valid"""
        if self._parent_pool:
            weakself = weakref.ref(self)
            
            self._weakref = weakref.ref(self._parent_pool._is_valid,
                                        lambda x: \
                                        _mark_weakpool_invalid(weakself))
        self._is_valid = lambda: 1
        
    def _mark_invalid(self):
        """Mark pool as invalid"""
        if self.valid():
            del self._is_valid
            
            del  self._parent_pool
            if hasattr(self, '_weakref'):
                del self._weakref

class SvnConnector(object):
    def __init__(self):
        self._version = None
        try:
            _import_svn()
        except ImportError:
            self.has_subversion = False
        else:
            self.has_subversion = True
            Pool()
            
    def get_supported_types(self):
        if self.has_subversion:
            yield('direct-svnfs', 4)
            yield('svnfs', 4)
            yield('svn', 2)
    
    def get_repository(self, dir, type=None, authname=None):
        """Return a `SubversionRepository`.
        
        The repository is wrapped in a `CachedRepository`, unless `type` is
        'direct-svnfs'.
        """
        
        if not self._version:
            self._version = self._get_version()
            #self.env.systeminfo.append(('Subversion', self._version))

        return SvnRepository(dir, None, None)
    
    def _get_version(self):
        version = (core.SVN_VER_MAJOR, core.SVN_VER_MINOR, core.SVN_VER_MICRO)
        version_string = '%d.%d.%d' % version + core.SVN_VER_TAG
        if version[0] < 1:
            raise Exception('Subversion >= 1.0 required: Found %(version)s',
                            version=version_string)
        return version_string
            

class SvnPropertyRenderer(object):
    def __init__(self):
        self._externals_maps = {}
    
    def match_property(self, name, mode):
        return name in ('svn:externals', 'svn:needs-lock') and 4 or 0
    
    def render_property(self, name, mode, context, props):
        if name == 'svn:externals':
            return self._render_externals(props[name])
        elif name == 'svn:needs-lock':
            return self._render_needslock(context)
    
    def _render_externals(self, prop):
        pass
    
    def _render_needslock(self, context):
        pass

class SvnRepository(object):
    def __init__(self, path, authz, log, options={}):
        self.log = log
        self.options = options
        self.pool = Pool()
        
        if isinstance(path, unicode):
            path = path.encode('utf-8')
        path = os.path.normpath(path).replace('\\', '/')
        self.path = repos.svn_repos_find_root_path(path, self.pool())
        if self.path is None:
            raise Exception('%(path)s does not appear to be a Subversion'
                            'Repository.' % {'path': path})
        
        self.repos = repos.svn_repos_open(self.path, self.pool())
        self.fs_ptr = repos.svn_repos_fs(self.repos)
        
        uuid = fs.get_uuid(self.fs_ptr, self.pool())
        name = 'svn:%s:%s' % (uuid, _from_svn(path))
        
        if self.path != path:
            self.scope = path[len(self.path):]
            if not self.scope[-1] == '/':
                self.scope += '/'
        else:
            self.scope = '/'
        assert self.scope[0] == '/'
        self.clear()
        
        self.youngest_rev = property(lambda x: x.get_youngest_rev())
    
    def clear(self, youngest_rev=None):
        self.youngest = None
        if youngest_rev is not None:
            self.youngest = self.normalize_rev(youngest_rev)
        self.oldest = None
    
    def __del__(self):
        self.close()
        
    def has_node(self, path, rev=None, pool=None):
        if not pool:
            pool = self.pool
        rev = self.normalize_rev(rev)
        rev_root = fs.revision_root(self.fs_ptr, rev, pool())
        node_type = fs.check_path(rev_root, _to_svn(self.scope, path), pool())
        return node_type in _kindmap
    
    def normalize_path(self, path):
        return _normalize_path(path)
    
    def normalize_rev(self, rev):
        if rev is None or isinstance(rev, basestring) and \
           rev.lower() in ('', 'head', 'latest', 'youngest'):
            return self.youngest_rev
        else:
            try:
                rev = int(rev)
                if rev <= self.youngest_rev:
                    return rev
            except (ValueError, TypeError):
                pass
            raise Exception('No such changeset: %d' % rev)

    def close(self):
        self.repos = self.fs_ptr = self.pool = None
    
    def _get_tags_or_branches(self, paths):
        """Retrieve known branches or tags."""
        pass
    
    def get_changeset(self, rev):
        rev = self.normalize_rev(rev)
        return SvnChangeset(rev, self.scope, self.fs_ptr, self.pool)
    
    def get_node(self, path, rev=None):
        path = path or ''
        
        if path and path[-1] == '/':
            path = path[:1]
        
        rev = self.normalize_rev(rev) or self.youngest_rev
        return SvnNode(path, rev, self, self.pool)
    
    def _history(self, svn_path, start, end, pool):
        """`svn_path` must be a full scope path, UTF-8 encoded string.
        
        Generator yielding `(path, rev)` pairs, where `path` is an `unicode`
        object.
        Must start with `(path, created_rev)`.
        """
        
        if start < end:
            start, end = end, start
        
        root = fs.revision_root(self.fs_ptr, start, pool())
        tmp1 = Pool(pool)
        tmp2 = Pool(pool)
        history_ptr = fs.node_history(root, svn_path, tmp1())
        cross_copies = 1
        while history_ptr:
            history_ptr = fs.history_prev(history_ptr, cross_copies, tmp2())
            tmp1.clear()
            tmp1, tmp2 = tmp2, tmp1
            if history_ptr:
                path, rev = fs.history_location(history_ptr, tmp2())
                tmp2.clear()
                if rev < end:
                    break
                path = _from_svn(path)
                yield path, rev
        del tmp1
        del tmp2
    
    def _previous_rev(self, rev, path='', pool=None):
        if rev > 1:
            try:
                for _, prev in self._history(_to_svn(self.scope, path),
                                             0, rev-1, pool or self.pool):
                    return prev
            except:
                pass
        return None
    
    def get_oldest_rev(self):
        if self.oldest is None:
            self.oldest = 1
        return self.oldest
    
    def get_youngest_rev(self):
        if not self.youngest:
            self.youngest = fs.youngest_rev(self.fs_ptr, self.pool())
            if self.scope != '/':
                for path, rev in self.history(_to_svn(self.scope),
                                              0, self.youngest, self.pool):
                    self.youngest = rev
                    break
        return self.youngest
    
    def previous_rev(self, rev, path=''):
        rev = self.normalize_path(rev)
        return self._previous_rev(rev, path)
    
    def next_rev(self, rev, path='', find_initial_rev=False):
        rev = self.normalize_path(rev)
        next = rev + 1
        youngest = self.youngest_rev
        subpool = Pool(self.pool)
        while next <= youngest:
            subpool.clear()
            try:
                for _, next in self._history(_to_svn(self.scope, path),
                                             rev+1, next, subpool):
                    return next
            except:
                if not find_initial_rev:
                    return next
            next += 1
        return None
    
    def rev_older_than(self, rev1, rev2):
        return self.normalize_rev(rev1) < self.normalize_rev(rev2)
    
    def get_path_history(self, path, rev=None, limit=None):
        path = self.normalize_path(path)
        rev = self.normalize_rev(rev)
        expect_deletion = False
        subpool = Pool(self.pool)
        numrevs = 0
        while rev and (not limit or numrevs < limit):
            subpool.clear()
            if self.has_node(path, rev, subpool):
                if expect_deletion:
                    numrevs += 1
                    yield path, rev+1, 'D'

                newer = None
                older = None
                for p, r in self._history(_to_svn(self.scope, path, 0, rev,
                                                  subpool)):
                    older = (_path_within_scope(self.scope, p), r, 'A')
                    rev = self._previous_rev(r, pool=subpool)
                    if newer:
                        numrevs += 1
                        if older[0] == path:
                            yield newer[0], newer[1], 'M'
                        else:
                            rev = self._previous_rev(newer[1], pool=subpool)
                            yield newer[0], newer[1], 'C'
                            older = (older[0], older[1], 'U')
                            break
                    newer = older
                    
                if older:
                    numrevs += 1
                    yield older
            else:
                expect_deletion = True
                rev = self._previous_rev(rev, pool=subpool)

    def get_changes(self, old_path, old_rev, new_path, new_rev,
                    ignore_ancestry=0):
        return
        old_node = new_node = None
        old_rev = self.normalize_rev(old_rev)
        new_rev = self.normalize_rev(new_rev)
        if self.has_node(old_path, old_rev):
            old_node = self.get_node(old_path, old_rev)
        else:
            raise Exception('No Such Node')
        
        if self.has_node(new_path, new_rev):
            new_node = self.get_node(new_path, new_rev)
        else:
            raise Exception('No Such Node')
        
        if new_node.kind != old_node.kind:
            raise Exception('Diff mismatch')
        
        subpool = Pool(self.pool)
            
                
class SvnNode(object):
    def __init__(self, path, rev, repos, pool=None, parent=None):
        self.path = path
        self.repos = repos
        self.fs_ptr = repos.fs_ptr
        self.scope = repos.scope
        self._scoped_svn_path = _to_svn(self.scope, path)
        self.pool = Pool(pool)
        self._requested_rev = rev
        pool = self.pool()
        
        if parent and parent._requested_rev == self._requested_rev:
            self.root = parent.root
        else:
            self.root = fs.revision_root(self.fs_ptr, rev, self.pool())
        node_type = fs.check_path(self.root, self._scoped_svn_path, pool)
        if not node_type in _kindmap:
            raise Exception('No such node')
        
        if _kindmap[node_type] == 'F':
            self.isdir = False
            self.isfile = True
        elif _kindmap[node_type] == 'D':
            self.isdir = True
            self.isfile = False

        
        cr = fs.node_created_rev(self.root, self._scoped_svn_path, pool)
        cp = fs.node_created_path(self.root, self._scoped_svn_path, pool)
        
        if _is_path_within_scope(self.scope, cp):
            self.created_rev = cr
            self.created_path = _path_within_scope(self.scope, _from_svn(cp))
        else:
            self.created_rev, self.created_path = rev, path
        self.rev = self.created_rev
        #TODO: check node id
    
    def get_content(self):
        if self.isdir:
            return None
        s = core.Stream(fs.file_contents(self.root, self._scoped_svn_path,
                                         self.pool()))
        
        s._pool = self.pool
        return s
    
    def get_entries(self):
        if self.isfile:
            return
        
        pool = Pool(self.pool)
        entries = fs.dir_entries(self.root, self._scoped_svn_path, pool())
        for item in entries.keys():
            path = posixpath.join(self.path, _from_svn(item))
            yield SvnNode(path, self._requested_rev, self.repos, self.pool,
                          self)
    
    def get_history(self, limit=None):
        newer = None
        older = None
        pool = Pool(self.pool)
        numrevs = 0
        for path, rev in self.repos._hisotry(self._scoped_svn_path, 0,
                                             self._requested_rev, pool):
            path = _path_within_scope(self.scope, path)
            if rev > 0 and path:
                older = (path, rev, 'A')
                if newer:
                    if newer[0] == older[0]:
                        change  = 'M'
                    else:
                        change = 'C'
                    newer = (newer[0], newer[1], change)
                    numrevs += 1
                    yield newer
                newer = older
            if limit and numrevs >= limit:
                break
        if newer:
            yield newer
    
    def get_annotations(self):
        annotations = []
        if self.isfile:
            def blame_receiver(line_no, reviison, author, date, line, pool):
                annotations.append(revision)
            try:
                rev = _svn_rev(self.rev)
                start = _svn_rev(0)
                repo_url = 'file:///%s/%s' % (self.repos.path.lstrip('/'),
                                              self._scoped_svn_path)
                from svn import client
                client.blame2(repo_url, rev, start, rev, blame_receiver,
                              client.create_context(), self.pool())
                
            except:
                raise Exception('svn blame failed')
        return annotations
    
    def get_properties(self):
        props = fs.node_proplist(self.root, self._scoped_svn_path, self.pool())
        for name, value in props.items():
            props[_from_svn(name)] = to_unicode(value, 'utf-8')
        return props
    
    def get_content_length(self):
        if self.isdir:
            return None
        return fs.file_length(self.root, self._scoped_svn_path, self.pool())
    
    def get_content_type(self):
        if self.isdir:
            return None
        return self._get_prop(core.SVN_PROP_MIME_TYPE)
    
    def get_last_modified(self):
        _date = fs.revision_prop(self.fs_ptr, self.created_rev,
                                 core.SVN_PROP_REVISION_DATE, self.pool())
        if not _date:
            return None
        
        return core.svn_time_from_cstring(_date, self.pool()) / 1000000
        
    def _get_prop(self, name):
        return fs.node_prop(self.root, self._scoped_svn_path, name, self.pool())

class SvnChangeset(object):
    def __init__(self, rev, scope, fs_ptr, pool=None):
        self.rev = rev
        self.scope = scope
        self.fs_ptr = fs_ptr
        self.pool = Pool(pool)
        try:
            self.message = self._get_prop(core.SVN_PROP_REVISION_LOG)
        except:
            raise('No such changeset')
        
        self.author = self._get_prop(core.SVN_PROP_REVISION_AUTHOR)
        self.message = self.message and to_unicode(self.message, 'utf-8')
        self.author = self.author and to_unicode(self.author, 'utf-8')
        _date = self._get_prop(core.SVN_PROP_REVISION_DATE)
        if _date:
            self.date = core.svn_time_from_cstring(_date, self.pool()) / 1000000
        else:
            self.date = None
    
    def get_properties(self):
        props = fs.revision_proplist(self.fs_ptr, self.rev, self.pool())
        properties = {}
        for k, v in props.iteritems():
            if k not in (core.SVN_PROP_REVISION_LOG, 
                         core.SVN_PROP_REVISION_AUTHOR,
                         core.SVN_PROP_REVISION_DATE):
                properties[k] = to_unicode(v)
        return properties
    
    def set_message(self, message):
        self._set_prop(core.SVN_PROP_REVISION_LOG, str(message))
    
    def get_changes(self):
        pool = Pool(self.pool)
        tmp = Pool(pool)
        root = fs.revision_root(self.fs_ptr, self.rev, pool())
        editor = repos.RevisionChangeCollector(self.fs_ptr, self.rev, pool())
        e_ptr, e_baton = delta.make_editor(editor, pool())
        repos.svn_repos_replay(root, e_ptr, e_baton, pool())
        
        idx = 0
        copies, deletions = {}, {}
        changes = []
        revroots = {}
        for path, change in editor.changes.items():
            if not (_is_path_within_scope(self.scope, path)):
                continue
            
            path = change.path
            base_path = change.base_path
            base_rev = change.base_rev
            
            if not (_is_path_within_scope(self.scope, base_path)):
                base_path, base_rev = None, -1
            
            if not path:
                if base_path:
                    if base_path in deletions:
                        continue
                    action = 'D'
                    deletions[base_path] = idx
                elif self.scope == '/':
                    action = 'E'
                else:
                    continue
            elif change.added or not base_path:
                action = 'A'
                if base_path and base_rev:
                    action = 'C'
                    copies[base_path] = idx
            else:
                action = 'E'
                if revroots.has_key(base_rev):
                    b_root = revroots[base_rev]
                else:
                    b_root = fs.revision_root(self.fs_ptr, base_rev, pool())
                    revroots[base_rev] = b_root
                tmp.clear()
                cbase_path = fs.node_created_path(b_root, base_path, tmp())
                cbase_rev = fs.node_created_rev(b_root, base_path, tmp())
                
                if _is_path_within_scope(self.scope, cbase_path):
                    base_path, base_rev = cbase_path, cbase_rev
            kind = _kindmap[change.item_kind]
            path = _path_within_scope(self.scope, _from_svn(path or base_path))
            base_path = _path_within_scope(self.scope, _from_svn(base_path))
            changes.append({'path': path, 'kind': kind, 'action': action,
                            'base_path': base_path, 'base_rev': base_rev})
            idx += 1
        
        moves = []
        for k,v in copies.items():
            if k in deletions:
                changes[v]['action'] = 'M'
                moves.append(deletions[k])
        offset = 0
        moves.sort()
        for i in moves:
            del changes[i - offset]
            offset += 1
        
        changes.sort()
        for change in changes:
            yield change

    def _set_prop(self, name, value):
        fs.change_rev_prop(self.fs_ptr, self.rev, name, value, self.pool())
    
    def _get_prop(self, name):
        return fs.revision_prop(self.fs_ptr, self.rev, name, self.pool())