import { useEffect, useState } from "react";
import useFetch from "../../hooks/useFetch"
import moment from 'moment'

function Prediction() {
  const [predictionDay, setPredictionDay] = useState([]);
  const [predictionHour, setPredictionHour] = useState([]);

  const [loading, makeRequest] = useFetch();

  async function fetchDataDay() {
    const data = await makeRequest("GET", "/prediction/update-count-day");
    const prediction = data[0]
    prediction.predict_day = moment(prediction.predict_day).format('DD/MM/YYYY')
    setPredictionDay(prediction)
    console.log(prediction)
  }

  async function fetchDataHour() {
    const data = await makeRequest("GET", "/prediction/update-count-hour");
    const prediction = data.map((row) => {
      const predict_hour = moment(row.predict_hour).format("DD/MM/YYYY HH:mm");
      return { ...row, predict_hour };
    });
    setPredictionHour(prediction)
    console.log(prediction)
  }

  useEffect(() => {
    fetchDataDay();
    fetchDataHour();
  }, []);

  useEffect(() => {
    let ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onmessage = e => {
      const message = JSON.parse(e.data);
      
      if (message.type === "refresh") {
        fetchDataDay();
        fetchDataHour();
      }
    };

    return () => {
      ws.close();
    }
  })

  return (
    <div className="flex gap-4 justify-center">
      <div className="bg-slate-200 p-5 rounded-lg basis-1/4 text-center flex flex-col shadow-md border">
        <div className="">
          <div>Số lượng cập nhật dự kiến</div>
          <strong>{predictionDay.predict_day}</strong>
        </div>
        <div className="text-4xl font-bold">
          <span>{predictionDay.predict_value}</span>
        </div>
      </div>
      <div className="rounded-lg flex flex-col w-3/4">
        <div className="bg-slate-200 p-1 rounded-lg shadow-md border">
          Số lượng cập nhật dự kiến trong các giờ tiếp theo
        </div>
        <div className="grow flex mt-3 gap-2">
          {predictionHour.map((predict, index) => (
            <div
              key={index}
              className="flex flex-col items-center bg-slate-200 p-2 rounded-lg basis-1/3 shadow-md border"
            >
              <div className="font-normal">{predict.predict_hour}</div>
              <div className="grow flex items-center text-4xl font-bold">
                {predict.predict_value}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Prediction;
