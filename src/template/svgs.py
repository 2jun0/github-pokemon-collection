def load_svg_template(path: str) -> str:
    with open(path) as f:
        svg = f.read()

    # swap {{ <-> {, { <-> {{
    svg = svg.replace("{{", "[[").replace("{", "{{").replace("[[", "{")
    return svg.replace("}}", "]]").replace("}", "}}").replace("]]", "}")


base = load_svg_template("templates/svgs/base.svg")
pokemon = load_svg_template("templates/svgs/pokemon.svg")
