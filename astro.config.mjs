import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// 운영 도메인: https://tteonamoa.org
export default defineConfig({
  site: "https://tteonamoa.org",
  integrations: [sitemap()],
});
