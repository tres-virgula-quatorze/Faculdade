import re

file_path = 'src/lib/components/Slides.svelte'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace {@const t = getT(X)} and the associated t inside the section
# A regex to match each {@const t = getT(X)} block and rename t -> tX
def rename_t(m):
    phase = m.group(1)
    return f'{{@const t{phase} = getT({phase})}}'

# We can just change {@const t = getT(1)} to {@const t1 = getT(1)}
content = re.sub(r'\{@const t = getT\((\d+)\)\}', rename_t, content)

# But wait, now all the inside variables are still using `t`.
# We need to change `t` to `tX` inside the section bounds.
# A better way is to wrap each slide section inside a block, like {#if true} or {#key i}, or <svelte:fragment>.
# No, we can just use string manipulation since we know where each section starts and ends.
# Better yet, if we wrap each section in {#if true} {@const t = getT(X)} ... {/if}, they get their own scope!
# Svelte allows {#if true} without penalty.
# Let's wrap each section.

# Wait, if we just replace {@const t = getT(X)} with {#if true}\n{@const t = getT(X)}, and then add {/if} after </section>
# Let's find </section> and add {/if} if it was part of a slide.

# Actually, doing it via a script might be tricky. Let's just rename t to tX everywhere.
def replace_slide_block(m):
    phase = m.group(1)
    body = m.group(2)
    # Replace t with t{phase} inside the body, but only as a standalone variable
    # like (t) or (t,
    body = re.sub(r'\bt\b', f't{phase}', body)
    return f'{{@const t{phase} = getT({phase})}}\n{body}'

# Match {@const t = getT(X)} up to the next {@const t = getT or end of file
pattern = r'\{@const t = getT\((\d+)\)\}\n(.*?)(?=\{@const t = getT|<\/div>\n<\/section>\n<\/div>)'
# Since we have `</div>\n</section>\n</div>`, we can use re.split
parts = re.split(r'\{@const t = getT\((\d+)\)\}', content)
new_content = parts[0]
for i in range(1, len(parts), 2):
    phase = parts[i]
    body = parts[i+1]
    # rename t to t{phase}
    body = re.sub(r'\bt\b', f't{phase}', body)
    new_content += f'{{@const t{phase} = getT({phase})}}{body}'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
