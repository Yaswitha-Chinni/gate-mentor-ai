import os
import glob

views_dir = 'views'
for filepath in glob.glob(os.path.join(views_dir, '*.py')):
    if '__init__' in filepath:
        continue
    
    content = None
    for enc in ['utf-8', 'utf-16']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break
        except Exception:
            pass
            
    if content is None:
        print(f"Failed to read {filepath}")
        continue
        
    lines = content.splitlines(keepends=True)
        
    new_lines = []
    
    import_lines = []
    other_lines = []
    for line in lines:
        if line.startswith('import ') or line.startswith('from '):
            import_lines.append(line)
        else:
            other_lines.append(line)
            
    while other_lines and other_lines[0].strip() == '':
        other_lines.pop(0)
        
    # Check if we already refactored it
    if any('def render():' in line for line in other_lines):
        print(f"Already refactored {filepath}")
        continue
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(import_lines)
        f.write('\n\ndef render():\n')
        for line in other_lines:
            f.write('    ' + line if line.strip() else '\n')
    print(f'Processed {filepath}')
