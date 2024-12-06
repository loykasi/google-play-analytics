import ForceGraph2D from "react-force-graph-2d";
import useFetch from "../hooks/useFetch"
import { useState, useEffect, useRef } from "react";

function Pattern6() {

  const [graphData, setGraphData] = useState(null);

  const [loading, makeRequest] = useFetch();
  async function fetchData() {
    const data = await makeRequest("GET", "/clustering/category");
    const nodeDegrees = {};
    data.links.forEach((link) => {
      nodeDegrees[link.source] = (nodeDegrees[link.source] || 0) + 1;
      nodeDegrees[link.target] = (nodeDegrees[link.target] || 0) + 1;
    });
    data.nodes.forEach((node) => {
      node.degree = nodeDegrees[node.id] || 0;
    });
    setGraphData(data)
  }

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="p-5 h-screen">
      <div className="h-full w- overflow-hidden">
        {graphData &&
        <ForceGraph2D
          width={2000}
          // height={100}
          graphData={graphData}
          nodeAutoColorBy="group"
          warmupTicks={100}
          cooldownTicks={0}
          nodeCanvasObjectMode={(node) => "after"}
          nodeRelSize={0}
          nodeCanvasObject={(node, ctx, globalScale) => {
            const nodeSize = Math.sqrt(node.degree);
            const label = node.id;
            const fontSize = 14/globalScale;
            ctx.font = `${fontSize}px Sans-Serif`;
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

            ctx.beginPath();
            ctx.arc(node.x, node.y, nodeSize / 2, 0, 2 * Math.PI, false);
            ctx.fill();

            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2  - nodeSize / 2 -1, ...bckgDimensions);

            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = node.color;
            ctx.fillText(label, node.x, node.y - nodeSize / 2 - 1);
          }}
          linkColor={() => "rgba(0, 0, 0, 0.1)"}
          enablePointerInteraction={false}
        />
        }
      </div>
    </div>
  );
}

export default Pattern6;
