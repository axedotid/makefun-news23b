// Node 22 entrypoint (standard library only). The image is rendered by build_image.py,
// which the agent authored and ran; this program copies the committed entry.png to
// /output/entry.png. The gate takes a whole PNG of at most 1 MiB and 1024x1024 pixels,
// and the judge sees exactly the bytes copied. Runs twice -> identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(out, { recursive: true });

const src = new URL('./entry.png', import.meta.url);
const dest = join(out, 'entry.png');
copyFileSync(src, dest);

// Fail loudly rather than silently shipping a bad entry.
const bytes = statSync(dest).size;
if (bytes === 0) throw new Error('entry.png is empty');
if (bytes > 1_048_576) throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB cap`);

// Validate the PNG structure, not just the size: a non-empty, under-cap file could
// still be the wrong format or the wrong dimensions. Check the 8-byte PNG signature,
// then read the IHDR chunk (always first) for the width/height.
const buf = readFileSync(dest);
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 24 || !buf.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error('entry.png is not a valid PNG (bad signature)');
}
if (buf.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png is missing the IHDR chunk');
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

console.log(`copied entry.png to ${dest} (${bytes} bytes, ${width}x${height} PNG)`);