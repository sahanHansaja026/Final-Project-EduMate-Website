import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    // Unit tests run in a plain Node environment. Install jsdom and set
    // "environment": "jsdom" here (or use a per-file @vitest-environment
    // comment) if a test needs DOM APIs.
    environment: "node",
    include: ["**/*.test.{ts,tsx}"],
    exclude: ["node_modules/**", ".next/**", "out/**", "build/**"],
  },
});
