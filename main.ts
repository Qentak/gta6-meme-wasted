// Hand-in packer: place POST.json (and meme.png, if present) in the output dir.
// Uses only Node's filesystem/path modules; no network calls or time reads.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const bot = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(out, { recursive: true });

const carry = (name: string, required: boolean) => {
  const from = join(bot, name);
  if (!existsSync(from)) {
    if (required) {
      console.error(`Missing ${name} in ${bot}; expected ${from}`);
      process.exit(1);
    }
    return;
  }
  try {
    writeFileSync(join(out, name), readFileSync(from));
  } catch (err) {
    console.error(`Could not copy ${from}: ${(err as Error).message}`);
    process.exit(1);
  }
};

carry("POST.json", true);
carry("meme.png", false);
