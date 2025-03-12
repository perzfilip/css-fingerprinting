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
        'Gill Sans',
        'HELV',
        'Haettenschweiler',
        'Helvetica Neue',
        'Humanst521 BT',
        'Leelawadee',
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
        'PMingLiU',
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

    html_template = """<div class=\"font-detection-wrapper\">\n    <div id=\"font-{id}-container\">\n        <p>{name}</p>\n    </div>\n    <p id=\"font-{id}-text\">mmmmmmmmmmlllllllllllllllllllllllllllllllllllllll</p>\n</div>\n"""

    css_template = """/* {name}, fallback */\n#font-{id}-container {{\n    container-type: inline-size;\n    container-name: font-{id}-container;\n}}\n\n#font-{id}-text {{\n    font-family: {name}, sans-serif;\n    font-size: 16px;\n    white-space: nowrap;\n    display: block;\n}}\n\n@container font-{id}-container (width > 100px) {{\n    p {{\n        background-color: blue;\n    }}\n}}\n\n"""

    html_content = "<html>\n<head>\n    <link rel=\"stylesheet\" type=\"text/css\" href=\"fonts.css\">\n</head>\n<body>\n"
    css_content = ""

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


if __name__ == '__main__':
    generate_font_rules()
