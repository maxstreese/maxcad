// Project pages: the part / in-context switch and the variant picker of each
// part (src/cadkit/site.py writes the markup and each part's variants as JSON).
for (const part of document.querySelectorAll(".part")) {
  const variants = JSON.parse(part.querySelector("script[type='application/json']").textContent);
  const viewer = part.querySelector("model-viewer");
  const buttons = [...part.querySelectorAll(".seg button")];
  const select = part.querySelector("select");
  let variant = variants[0];
  let view = "part";

  const show = () => {
    const src = view === "context" && variant.context ? variant.context : variant.glb;
    if (viewer.getAttribute("src") !== src) viewer.setAttribute("src", src);
    viewer.setAttribute("alt", `3D model of ${variant.name}${view === "context" ? ", in context" : ""}`);
    for (const b of buttons) b.setAttribute("aria-pressed", String(b.dataset.view === view));
    part.querySelector("[data-f='size']").textContent = variant.size;
    part.querySelector("[data-f='volume']").textContent = variant.volume;
    for (const a of part.querySelectorAll(".downloads a")) {
      const file = variant.files[a.dataset.kind];
      a.setAttribute("href", file.href);
      a.querySelector("small").textContent = file.size;
    }
    for (const cell of part.querySelectorAll("[data-opt]")) cell.textContent = variant.options[cell.dataset.opt];
  };

  for (const b of buttons) b.addEventListener("click", () => { view = b.dataset.view; show(); });
  if (select) select.addEventListener("change", () => { variant = variants[select.selectedIndex]; show(); });
}
