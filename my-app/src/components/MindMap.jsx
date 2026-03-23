import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

export default function MindMap({ data }) {
  const ref = useRef();

  useEffect(() => {
    if (!data) return;

    const width = 1000;
    const dx = 70;   // more vertical spacing
    const dy = 200;  // more horizontal spacing

    d3.select(ref.current).selectAll("*").remove();

    const root = d3.hierarchy(data);

    const tree = d3.tree().nodeSize([dx, dy]);
    tree(root);

    let x0 = Infinity;
    let x1 = -x0;

    root.each(d => {
      if (d.x > x1) x1 = d.x;
      if (d.x < x0) x0 = d.x;
    });

    const svg = d3.select(ref.current)
      .append("svg")
      .attr("viewBox", [0, 0, width, x1 - x0 + dx * 2])
      .style("font", "13px Inter, sans-serif")
      .style("user-select", "none");

    const g = svg.append("g")
      .attr("transform", `translate(${dy / 2},${dx - x0})`);

    // ================= LINKS (SMOOTH CURVE) =================
    g.append("g")
      .attr("fill", "none")
      .attr("stroke", "#6366f1") // softer indigo
      .attr("stroke-opacity", 0.5)
      .attr("stroke-width", 2)
      .selectAll("path")
      .data(root.links())
      .join("path")
      .attr("d", d3.linkHorizontal()
        .x(d => d.y)
        .y(d => d.x)
      )
      .attr("stroke-linecap", "round");

    // ================= NODES =================
    const node = g.append("g")
      .selectAll("g")
      .data(root.descendants())
      .join("g")
      .attr("transform", d => `translate(${d.y},${d.x})`);

    // NODE STYLE BASED ON DEPTH
    node.append("circle")
      .attr("r", d => d.depth === 0 ? 14 : d.depth === 1 ? 10 : 7)
      .attr("fill", d =>
        d.depth === 0 ? "#22c55e" :
        d.depth === 1 ? "#3b82f6" :
        "#a78bfa"
      )
      .attr("stroke", "#0f172a")
      .attr("stroke-width", 2)
      .style("filter", "drop-shadow(0px 2px 6px rgba(0,0,0,0.5))");

    // ================= TEXT WRAP =================
    function wrap(text, width) {
      text.each(function () {
        const textSel = d3.select(this);
        const words = textSel.text().split(/\s+/).reverse();
        let word, line = [], lineNumber = 0;
        const lineHeight = 1.2;
        const y = textSel.attr("y");
        let tspan = textSel.text(null)
          .append("tspan")
          .attr("x", 0)
          .attr("y", y);

        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(" "));
          if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
            line = [word];
            tspan = textSel.append("tspan")
              .attr("x", 0)
              .attr("y", y)
              .attr("dy", ++lineNumber * lineHeight + "em")
              .text(word);
          }
        }
      });
    }

    node.append("text")
      .attr("dy", "0.35em")
      .attr("x", d => d.children ? -18 : 18)
      .attr("text-anchor", d => d.children ? "end" : "start")
      .attr("fill", "#e5e7eb")
      .style("font-size", d => d.depth === 0 ? "14px" : "12px")
      .style("font-weight", d => d.depth === 0 ? "600" : "400")
      .text(d => d.data.name)
      .call(wrap, 140);

    // ================= HOVER EFFECT =================
    node.on("mouseover", function () {
      d3.select(this).select("circle")
        .transition()
        .duration(200)
        .attr("r", 16);
    });

    node.on("mouseout", function () {
      d3.select(this).select("circle")
        .transition()
        .duration(200)
        .attr("r", d => d.depth === 0 ? 14 : d.depth === 1 ? 10 : 7);
    });

    // ================= ZOOM =================
    svg.call(
      d3.zoom().scaleExtent([0.6, 2]).on("zoom", (event) => {
        g.attr("transform", event.transform);
      })
    );

  }, [data]);

  return (
    <div className="bg-gradient-to-br from-white/5 to-white/0 p-6 rounded-2xl border border-white/10 mt-6 shadow-lg">

      <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
        🧠 Mind Map
        <span className="text-xs text-gray-400">(Zoom & drag)</span>
      </h2>

      <div className="overflow-hidden rounded-xl">
        <div ref={ref}></div>
      </div>

    </div>
  );
}