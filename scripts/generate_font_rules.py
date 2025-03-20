import os

def generate_font_rules():
    fonts = [
        'sans-serif-thin',
        'ARNO PRO',
        'Agency FB',
        'Arabic Typesetting',
        'Arial Unicode MS',
        'AvantGarde Bk BT',
        'BankGothic Md BT',
        'Batang',
        'Bitstream Vera Sans Mono',
        'Calibri',
        'Century',
        'Century Gothic',
        'Clarendon',
        'EUROSTILE',
        'Franklin Gothic',
        'Futura Bk BT',
        'Futura Md BT',
        'GOTHAM',
        'Gill Sans MT',
        'HELV',
        'Haettenschweiler',
        'Helvetica Neue',
        'Humanst521 BT',
        'Leelawadee UI',
        'Letter Gothic',
        'Levenim MT',
        'Lucida Bright',
        'Lucida Sans',
        'Menlo',
        'MS Mincho',
        'MS Outlook',
        'MS Reference Specialty',
        'MS UI Gothic',
        'MT Extra',
        'MYRIAD PRO',
        'Marlett',
        'Meiryo UI',
        'Microsoft Uighur',
        'Minion Pro',
        'Monotype Corsiva',
        'PMingLiU-ExtB',
        'Pristina',
        'SCRIPTINA',
        'Segoe UI Light',
        'Serifa',
        'SimHei',
        'Small Fonts',
        'Staccato222 BT',
        'TRAJAN PRO',
        'Univers CE 55 Medium',
        'Vrinda',
        'ZWAdobeF'
    ]

    html_template = """<div class=\"font-detection-wrapper\">\n    <div id=\"font-{id}-container\">\n        <p>{name}</p>\n    </div>\n    <p id=\"font-{id}-text\">mmMwWLliI0O&1mmMwWLliI0O&1</p>\n</div>\n"""

    css_template = """/* {name}, fallback */\n#font-{id}-container {{\n    container-type: inline-size;\n    container-name: font-{id}-container;\n}}\n\n#font-{id}-text {{\n    font-family: \"{name}\", Arial, sans-serif;\n    font-size: 16px;\n    white-space: nowrap;\n    display: block;\n}}\n\n@container font-{id}-container not (256px < width < 257px) {{\n    p {{\n        background-image: url(\"/font-detection?font={name}\") !important;\n    }}\n}}\n\n"""

    html_content = "<html>\n<head>\n    <link rel=\"stylesheet\" type=\"text/css\" href=\"fonts.css\">\n</head>\n<body>\n"
    css_content = """
#font-detection {
    font-family: Arial, sans-serif;
}

.tested-font {
    background-color: blue;
}

.font-detection-wrapper {
    width: fit-content;
}
    """

    for font in fonts:
        font_id = font.lower().replace(" ", "-")
        html_content += html_template.format(id=font_id, name=font)
        css_content += css_template.format(id=font_id, name=font)

    html_content += "</body>\n</html>"

    with open("fonts.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    with open("fonts.css", "w", encoding="utf-8") as css_file:
        css_file.write(css_content)

    print("HTML and CSS files generated successfully!")


def generate_css_rules_env_9(width_start, width_end, height_start, height_end, container_name="env-9-container", attr_name="env-9", output_folder="outputs", output_file="generated.css"):
    css_rules = ""

    for px in range(width_start, width_end + 1):
        rule = (f"@container {container_name} (min-width: {px}px) {{\n"
                f"    p#env-9-width {{\n"
                f"        background-image: url(\"/fingerprint?env-9-width={px}\");\n"
                f"    }}\n"
                f"}}\n\n")
        css_rules += rule

    for px in range(height_start, height_end + 1):
        rule = (f"@container {container_name} (min-height: {px}px) {{\n"
                f"    p#env-9-height {{\n"
                f"        background-image: url(\"/fingerprint?env-9-height={px}\");\n"
                f"    }}\n"
                f"}}\n\n")
        css_rules += rule

    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, output_file), "w") as f:
        f.write(css_rules)


def generate_css_viewport(width_start, width_end, height_start, height_end, container_name="viewport", output_folder="outputs", output_file="viewport.css"):
    css_rules = ""

    for px in range(width_start, width_end + 1):
        rule = (f"@container {container_name} (min-width: {px}px) {{\n"
                f"    p#viewport-width {{\n"
                f"        display: block;\n"
                f"        background-image: url(\"/fingerprint?viewport_width={px}\");\n"
                f"    }}\n"
                f"}}\n\n")
        css_rules += rule

    for px in range(height_start, height_end + 1):
        rule = (f"@container {container_name} (min-height: {px}px) {{\n"
                f"    p#viewport-height {{\n"
                f"        display: block;\n"
                f"        background-image: url(\"/fingerprint?viewport_height={px}\");\n"
                f"    }}\n"
                f"}}\n\n")
        css_rules += rule

    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, output_file), "w") as f:
        f.write(css_rules)

if __name__ == '__main__':
    # generate_font_rules()
    # generate_css_rules_env_9(500, 700, 50, 150)
    generate_css_viewport(1, 100, 1, 100)
