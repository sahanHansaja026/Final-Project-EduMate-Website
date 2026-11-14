import { describe, expect, it } from "vitest";

import { cn } from "./utils";

describe("cn", () => {
  it("joins class names into a single string", () => {
    expect(cn("flex", "items-center", "gap-2")).toBe("flex items-center gap-2");
  });

  it("ignores falsy values", () => {
    expect(cn("text-sm", false, null, undefined, "", "font-bold")).toBe(
      "text-sm font-bold",
    );
  });

  it("supports arrays and conditional objects", () => {
    expect(cn(["flex", { hidden: false, "items-center": true }])).toBe(
      "flex items-center",
    );
  });

  it("keeps the last conflicting Tailwind utility", () => {
    expect(cn("px-2", "px-4")).toBe("px-4");
    expect(cn("bg-red-500", "bg-blue-500")).toBe("bg-blue-500");
  });
});
