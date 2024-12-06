import Chart1 from "../components/Pattern1/Chart1";
import Chart2 from "../components/Pattern1/Chart2";
import Prediction from "../components/Pattern1/Prediction";

function Pattern1() {
  return (
    <div className="p-5">
      <Prediction />

      <div className="flex gap-4 mt-4">
        <Chart1 />
        <Chart2 />
      </div>
    </div>
  );
}

export default Pattern1;
