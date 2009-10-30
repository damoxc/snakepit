import logging
from difflib import SequenceMatcher, IS_CHARACTER_JUNK

log = logging.getLogger(__name__)

def _get_change_extent(str1, str2):
    """
    Determines the extent of differences between two strings. Returns a tuple
    containing the offset at which the changes start, and the negative offset
    at which the changes end. If the two strings have neither a common prefix
    nor a common suffix, (0, 0) is returned.
    """
    start = 0
    limit = min(len(str1), len(str2))
    while start < limit and str1[start] == str2[start]:
        start += 1
    end = -1
    limit = limit - start
    while -end <= limit and str1[end] == str2[end]:
        end -= 1
    return (start, end + 1)

class Diff(object):
    def __init__(self, old, new, **kwargs):
        self.old = old.splitlines()
        self.new = new.splitlines()
        self.surrounding = kwargs.get('surrounding', 2)
        self.blank_lines = kwargs.get('blank_lines', False)
        self.case_changes = kwargs.get('case_changes', False)
        self.whitespace = kwargs.get('whitespace', False)
        
        junk = self.whitespace and IS_CHARACTER_JUNK or None        
        self.diff = SequenceMatcher(junk, self.old, self.new)
    
    def do_diff(self):
        if self.surrounding > -1:
            return self.__partial_diff()
        else:
            return self.__full_diff()
    
    def __partial_diff(self):
        return map(self.parse_section,
            self.diff.get_grouped_opcodes(self.surrounding))
    
    def __full_diff(self):
        return [self.parse_section(self.diff.get_opcodes())]
    
    def parse_section(self, section):
        lines = []
        for change_type, start_old, end_old, start_new, end_new in section:
            if change_type == 'replace':
                lines.extend(self.handle_replace(xrange(start_old, end_old),
                    xrange(start_new, end_new)))
            elif change_type == 'insert':
                lines.extend(self.handle_insert(xrange(start_new, end_new)))
            elif change_type == 'delete':
                lines.extend(self.handle_delete(xrange(start_old, end_old)))
            elif change_type == 'equal':
                lines.extend(self.handle_equal(xrange(start_old, end_old),
                    xrange(start_new, end_new)))
        return lines
    
    def handle_replace(self, deleted_lines, inserted_lines):
        raise NotImplementedError()
    
    def handle_insert(self, inserted_lines):
        length = len(inserted_lines) - 1
        for index, line in enumerate(inserted_lines):
            change_type = ('insert', (index is 0 and 'start' or '') + (index is
                length and ' end' or ''))
            yield change_type, '', line+1, self.new[line]
    
    def handle_delete(self, deleted_lines):
        length = len(deleted_lines) - 1
        for index, line in enumerate(deleted_lines):
            change_type = ('delete', (index is 0 and 'start' or '') + (index is
                length and ' end' or ''))
            yield change_type, line + 1, '', self.old[line]
    
    def handle_equal(self, old_lines, new_lines):
        for index, line in enumerate(old_lines):
            change_type = ('equal', index is 0 and 'start' or 'end')
            new_line = new_lines[index]
            yield change_type, line + 1, new_line + 1, self.old[line]
        

class InlineDiff(Diff):
    def handle_replace(self, deleted_lines, inserted_lines):
        length = len(inserted_lines) - 1
            
        log.debug('Handling replace (del=%d:%d;ins=%d:%d)', deleted_lines[0],
            deleted_lines[-1], inserted_lines[0], inserted_lines[-1])
        
        do_line_diff = len(deleted_lines) == len(inserted_lines)

        for index, line in enumerate(deleted_lines):
            change_type = ('delete', index is 0 and 'start' or '')
            
            # If we've run out of inserted lines to diff against we just want
            # to yield our result now rather than raise an Exception.
            if index >= len(inserted_lines):
                yield change_type, line + 1, '', self.old[line]
                continue
            
            old_line = self.old[line]
            new_line = self.new[inserted_lines[index]]
            
            log.debug('Old line: %s', old_line)
            
            if not do_line_diff:
                yield change_type, line + 1, '', self.old[line]
                continue
            
            start, end = _get_change_extent(old_line, new_line)
            characters = [
                ('equal', old_line[:start]),
                ('del', old_line[start:end]),
                ('equal', old_line[end:])
            ]
            yield change_type, line + 1, '', characters
        
        for index, line in enumerate(inserted_lines):
            change_type = ('insert', index is length and 'end' or '')
            
            # If we've run out of deleted lines to diff against we just want
            # to yield our result now rather than raise an Exception.
            if index >= len(deleted_lines):
                yield change_type, '', line + 1, self.new[line]
                continue

            old_line = self.old[deleted_lines[index]]
            new_line = self.new[line]
            
            log.debug('New line: %s', old_line)
            
            if not do_line_diff:
                yield change_type, '', line + 1, self.new[line]
                continue
            
            start, end = _get_change_extent(old_line, new_line)
            characters = (
                ('equal', new_line[:start]),
                ('ins', new_line[start:end]),
                ('equal', new_line[end:])
            )
            yield change_type, '', line + 1, characters

class SideBySideDiff(Diff):
    def handle_replace(self, deleted_lines, inserted_lines):
        if len(deleted_lines) > len(inserted_lines):
            length = len(deleted_lines) - 1
        else:
            length = len(inserted_lines) - 1
        
        for index in xrange(0, length + 1):
            change_type = ('replace', (index is 0 and 'start' or '') + (index is
                length and ' end' or ''))
            
            if index < len(deleted_lines):
                old_line_num = deleted_lines[index] + 1
                old_line = self.old[deleted_lines[index]]
            else:
                old_line_num = ''
                old_line = ''
            
            if index < len(inserted_lines):
                new_line_num = inserted_lines[index] + 1
                new_line = self.new[inserted_lines[index]]
            else:
                new_line_num = ''
                new_line = ''
                
            start, end = _get_change_extent(old_line, new_line)
            old_characters = (
                ('equal', old_line[:start]),
                ('del', old_line[start:end]),
                ('equal', old_line[end:])
            )
            new_characters = (
                ('equal', new_line[:start]),
                ('ins', new_line[start:end]),
                ('equal', new_line[end:])
            )
            
            yield change_type, old_line_num, new_line_num, old_characters, \
                  new_characters