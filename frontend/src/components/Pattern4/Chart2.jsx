import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { CONFIG_PLOT } from "../../_constant";
import useFetch from "../../hooks/useFetch"

function Chart1() {
  const [dataGame, setDataGame] = useState([]);

  const [loading, makeRequest] = useFetch();
  async function fetchData() {
    const data = await makeRequest("GET", "/group/genre/game/30");
    setDataGame(data)
  }
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Plot
      className="w-full h-full"
      data={[
        {
          type: "bar",
          y: dataGame.map((i) => i.genre),
          x: dataGame.map((i) => i.count),
          text: dataGame.map((i) => i.count),
          textposition: "top",
          orientation: "h",
        },
      ]}
      layout={{
        title: "Game",
        xaxis: { title: "Lượt cập nhật" },
        yaxis: {
          ticklabelposition: "inside",
          autorange: "reversed"
        },
      }}
      config={CONFIG_PLOT}
    />
  );
}

export default Chart1;
