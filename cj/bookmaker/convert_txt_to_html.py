def convert_to_html(text_file: str):
    """
    Convert a TXT file to a HTML file.
    """
    # Read the file contents
    with open(text_file, 'r', encoding='utf8') as file:
        lines = file.readlines()

    html = ""

    for i in range(len(lines)):
        # Specific case for the first line
        if i == 0:
            html += "<h3>" + lines[i] + "</h3>"
            continue

        pre_line = lines[i - 1].strip()
        line = lines[i].strip()
        next_line = lines[i + 1].strip() if i < len(lines) - 1 else ""

        if len(line) == 0 and (len(pre_line) == 0 or len(next_line) == 0):
            html += "<br>"
            continue
            
        if len(pre_line) == 0 and len(next_line) == 0:
            html += "<p>" + line + "</p>"
        elif len(pre_line) == 0 and len(next_line) > 0:
            html += "<p>" + line
        elif len(pre_line) > 0 and len(next_line) == 0:
            html += " " + line + "</p>"
        else:
            html += " " + line

    # Write the contents to a HTML file
    with open(text_file.replace('.txt', '.html'), 'w', encoding='utf8') as file:
        file.write(html)


if __name__ == '__main__':
    convert_to_html('captainjapan/source/novels/Mushoku Tensei Redundancy/32/Chapter 33.txt')
