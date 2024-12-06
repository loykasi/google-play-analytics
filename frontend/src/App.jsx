import { Routes, Route, Navigate, useLocation, Link } from "react-router-dom";
import "./App.css";
import Pattern1 from "./pages/Pattern1";
import Pattern2 from "./pages/Pattern2";
import Pattern3 from "./pages/Pattern3";
import Pattern4 from "./pages/Pattern4";
import Pattern5 from "./pages/Pattern5";
import Pattern6 from "./pages/Pattern6";

const links = [
  {
    label: "Cập nhật mới",
    to: "/page-1",
    active: "!text-[#4285f4]  bg-[#4285f4] border-r-[#4285f4] border-r-2",
  },
  {
    label: "Phân tích phổ biến",
    to: "/page-2",
    active: "!text-[#34a853]  bg-[#34a853] border-r-[#34a853] border-r-2",
  },
  {
    label: "Phân tích liên hệ",
    to: "/page-3",
    active: "!text-[#ea4335]  bg-[#ea4335] border-r-[#ea4335] border-r-2",
  },
  {
    label: "Danh mục phổ biến",
    to: "/page-4",
    active: "!text-[#fbbc04]  bg-[#fbbc04] border-r-[#fbbc04] border-r-2",
  },
  {
    label: "Phân nhóm danh mục",
    to: "/page-5",
    active: "!text-gray-600  bg-gray-600 border-r-gray-600 border-r-2",
  },
  {
    label: "Sơ đồ danh mục",
    to: "/page-6",
    active: "!text-gray-600  bg-gray-600 border-r-gray-600 border-r-2",
  },
];

export default function App() {
  const localtion = useLocation();

  return (
    <div className="flex">
      <div className="w-64 flex-none">
        <div className="sticky top-0 left-0 h-screen shadow-md">
          <div className="p-4 ml-2 mb-4 flex items-center">
            <svg
              className="size-10 inline-block mr-2"
              aria-hidden="true"
              viewBox="0 0 40 40"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path fill="none" d="M0,0h40v40H0V0z"></path>
              <g>
                <path
                  d="M19.7,19.2L4.3,35.3c0,0,0,0,0,0c0.5,1.7,2.1,3,4,3c0.8,0,1.5-0.2,2.1-0.6l0,0l17.4-9.9L19.7,19.2z"
                  fill="#EA4335"
                ></path>
                <path
                  d="M35.3,16.4L35.3,16.4l-7.5-4.3l-8.4,7.4l8.5,8.3l7.5-4.2c1.3-0.7,2.2-2.1,2.2-3.6C37.5,18.5,36.6,17.1,35.3,16.4z"
                  fill="#FBBC04"
                ></path>
                <path
                  d="M4.3,4.7C4.2,5,4.2,5.4,4.2,5.8v28.5c0,0.4,0,0.7,0.1,1.1l16-15.7L4.3,4.7z"
                  fill="#4285F4"
                ></path>
                <path
                  d="M19.8,20l8-7.9L10.5,2.3C9.9,1.9,9.1,1.7,8.3,1.7c-1.9,0-3.6,1.3-4,3c0,0,0,0,0,0L19.8,20z"
                  fill="#34A853"
                ></path>
              </g>
            </svg>
            <span className="text-xl font-semibold text-gray-600">
              Google Play
            </span>
          </div>
          <div className="flex flex-col space-y-2">
            {links.map((link) => (
              <Link
                key={link.label}
                to={link.to}
                className={`pl-6 py-2 font-medium text-gray-600 bg-opacity-10 hover:text-black 
                    ${link.to === localtion.pathname && link.active} `}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
      <div className="flex-1 bg-gray-50 overflow-x-hidden">
        <Routes>
          <Route path="/" element={<Navigate to="/page-1" />} />
          <Route path="/page-1" element={<Pattern1 />} />
          <Route path="/page-2" element={<Pattern2 />} />
          <Route path="/page-3" element={<Pattern5 />} />
          <Route path="/page-4" element={<Pattern4 />} />
          <Route path="/page-5" element={<Pattern3 />} />
          <Route path="/page-6" element={<Pattern6 />} />
          <Route path="*" element={<h1>Error: 404 Not Found</h1>} />
        </Routes>
      </div>
    </div>
  );
}
