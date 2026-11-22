// Injects the shared footer (assets/footer.html) into every HTML page on the server.
// If anything fails, the page's own footer is served unchanged.
export async function onRequest(context) {
  const response = await context.next();
  const type = response.headers.get("content-type") || "";
  if (!type.includes("text/html")) return response;
  try {
    const url = new URL(context.request.url);
    const footerRes = await context.env.ASSETS.fetch(new URL("/assets/footer.html", url.origin));
    if (!footerRes.ok) return response;
    const footerHtml = await footerRes.text();
    if (!footerHtml.includes("clean-footer")) return response;
    const out = new HTMLRewriter()
      .on("footer.clean-footer", {
        element(el) { el.replace(footerHtml, { html: true }); }
      })
      .transform(response);
    // The page body changes when footer.html changes, so the original ETag must not be reused.
    const headers = new Headers(out.headers);
    headers.delete("ETag");
    headers.delete("Last-Modified");
    headers.set("Cache-Control", "public, max-age=0, must-revalidate");
    return new Response(out.body, { status: out.status, statusText: out.statusText, headers });
  } catch (e) {
    return response;
  }
}
