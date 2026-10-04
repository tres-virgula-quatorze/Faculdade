import re

file_path = 'src/lib/components/Slides.svelte'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# First, undo the t1, t2 -> t renaming
# Every {@const tX = getT(X)} becomes {#if true}\n{@const t = getT(X)}
# We have to find the end of the section and insert {/if}

def replacer(m):
    num = m.group(1)
    return f'{{#if true}}\n  {{@const t = getT({num})}}'

content = re.sub(r'\{@const t\d+ = getT\((\d+)\)\}', replacer, content)

# Also fix the <section> tags that still have t
content = re.sub(r't\d+', 't', content)

# Now we need to append {/if} after each slide section.
# A slide section ends with </div>\n  </section>
content = re.sub(r'(<\/div>\s*<\/section>)', r'\1\n{/if}', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
