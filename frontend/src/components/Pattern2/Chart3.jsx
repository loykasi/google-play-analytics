import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import useFetch from "../../hooks/useFetch"
import { CONFIG_PLOT } from "../../_constant";

const test = ["Ngày", "Giờ"];

function Chart3() {
  const [loading, makeRequest] = useFetch();
  const [update, setUpdate] = useState([]);
  const [showChart, setShowChart] = useState(0);

  async function fetchData() {
    const data = await makeRequest("GET", "/group/day/30");
    setUpdate(data)
  }

  async function fetchDataHour() {
    const data = await makeRequest("GET", "/group/hour/800");
    setUpdate(data)
  }

  useEffect(() => {
    fetchData()
  }, []);

  useEffect(() => {
    if (showChart == 0) {
      fetchData()
    } else {
      fetchDataHour()
    }
  }, [showChart])

  useEffect(() => {
    let ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onmessage = e => {
      const message = JSON.parse(e.data);
      
      if (message.type === "refresh") {
        fetchData();
      }
    };

    return () => {
      ws.close();
    }
  })

  return (
    <div className="bg-slate-200 p-2 rounded-lg mt-4 ">
      {test.map((value, index) => (
        <span
          key={value}
          className={`px-4 py-1 rounded-t-md hover:bg-blue-200 cursor-pointer ${
            showChart === index && "!bg-blue-400 text-white"
          }`}
          onClick={() => setShowChart(index)}
        >
          {value}
        </span>
      ))}
      <Plot
        className="w-full h-[calc((100vh-140px)/2)]"
        data={[
          {
            x: showChart == 0? update.map((item) => item.date) : update.map((item) => item.date_hour),
            y: update.map((item) => item.app),
            name: "Ứng dụng",
            type: "bar",
            text: update.map((item) => item.app).map(String),
            textposition: "top center",
            mode: "lines+markers+text",
          },
          {
            x: showChart == 0? update.map((item) => item.date) : update.map((item) => item.date_hour),
            y: update.map((item) => item.game),
            name: "Trò chơi",
            type: "bar",
            text: update.map((item) => item.game).map(String),
            textposition: "top center",
            mode: "lines+markers+text",
          },
        ]}
        layout={{
          barmode: "group",
          title: "Lịch sử cập nhật",
          xaxis: {
            autorange: true
            // range: ["2024-10-20", "2024-11-15"],
          },
        }}
        config={CONFIG_PLOT}
      />
      
    </div>
  );
}

export default Chart3;
