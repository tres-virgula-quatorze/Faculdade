import re

slides_file = 'src/lib/components/Slides.svelte'
with open(slides_file, 'r', encoding='utf-8') as f:
    slides_content = f.read()

slides_content = slides_content.replace("\\'auto\\'", "'auto'")
slides_content = slides_content.replace("\\'none\\'", "'none'")

with open(slides_file, 'w', encoding='utf-8') as f:
    f.write(slides_content)
