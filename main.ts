// Node 22 entrypoint (standard library only). The image is rendered by build_image.py,
// which the agent authored and ran; this program copies the committed entry.png to
// /output/entry.png. The gate takes a whole PNG of at most 1 MiB and 1024x1024 pixels,
// and the judge sees exactly the bytes copied. Runs twice -> identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(out, { recursive: true });

const dest = join(out, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);

// Fail loudly rather than silently shipping a bad entry.
const bytes = statSync(dest).size;
if (bytes === 0) throw new Error('entry.png is empty');
if (bytes > 1_048_576) throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB cap`);
console.log(`copied entry.png to ${dest} (${bytes} bytes)`);