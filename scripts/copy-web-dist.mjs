import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const sourceDir = resolve(rootDir, "apps/web/dist");
const outputDir = resolve(rootDir, "dist");

if (!existsSync(sourceDir)) {
  throw new Error(`Web build output was not found: ${sourceDir}`);
}

rmSync(outputDir, { force: true, recursive: true });
mkdirSync(outputDir, { recursive: true });
cpSync(sourceDir, outputDir, { recursive: true });

console.log(`Copied ${sourceDir} to ${outputDir}`);
