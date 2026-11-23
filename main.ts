// Node 22 entrypoint (standard library only). The image is rendered by build_image.py,
// which the agent authored and ran; this program copies the committed entry.png to
// /output/entry.png. The gate takes a whole PNG of at most 1 MiB and 1024x1024 pixels,
// and the judge sees exactly the bytes copied. Runs twice -> identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(out, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(out, 'entry.png'));
console.log('copied entry.png to', out);