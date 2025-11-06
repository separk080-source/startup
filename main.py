import streamlit as st
src/
 ├─ App.jsx
 ├─ pages/
 │   ├─ Home.jsx
 │   ├─ MBTISelect.jsx
 │   ├─ Test.jsx
 │   └─ Result.jsx
 ├─ components/
 │   └─ CharacterCard.jsx
 ├─ data/
 │   └─ characters.js
 └─ main.jsx
export const characters = {
  F: [
    { id: 1, name: "따뜻한 유령", description: "감정에 민감하고 남을 잘 위로해요 👻" },
    { id: 2, name: "소심한 유령", description: "사람 마음을 잘 읽지만 상처도 잘 받아요 👻" },
    { id: 3, name: "밝은 유령", description: "항상 긍정적으로 사람을 대해요 👻" },
    { id: 4, name: "감정마스터 유령", description: "감정을 자유자재로 다루는 유령이에요 👻" },
  ],
  T: [
    { id: 1, name: "논리 그림자", description: "이성적이고 명확하게 생각해요 🩶" },
    { id: 2, name: "냉철한 그림자", description: "결정을 빠르게 내리는 현실주의자 🩶" },
    { id: 3, name: "분석가 그림자", description: "모든 걸 논리적으로 분석해요 🩶" },
    { id: 4, name: "전략가 그림자", description: "논리와 통찰의 달인이에요 🩶" },
  ],
};
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen text-center bg-gradient-to-b from-indigo-200 to-white">
      <h1 className="text-4xl font-bold mb-4">맞춤형 대화 도우미</h1>
      <p className="text-gray-600 mb-8">
        당신의 대화 스타일에 맞는 캐릭터를 만나보세요!
      </p>
      <button
        onClick={() => navigate("/mbti")}
        className="bg-indigo-500 text-white px-6 py-3 rounded-lg hover:bg-indigo-600 transition"
      >
        시작하기
      </button>
    </div>
  );
}
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function MBTISelect() {
  const navigate = useNavigate();
  const [selected, setSelected] = useState(null);

  const handleNext = () => {
    if (selected) navigate(`/test?type=${selected}`);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-b from-purple-100 to-white">
      <h2 className="text-3xl font-bold mb-6">당신의 MBTI 성향은?</h2>
      <div className="flex gap-6">
        <button
          className={`px-6 py-3 rounded-lg border-2 ${
            selected === "F" ? "bg-pink-300 border-pink-500" : "border-pink-300"
          }`}
          onClick={() => setSelected("F")}
        >
          감정형 (F)
        </button>
        <button
          className={`px-6 py-3 rounded-lg border-2 ${
            selected === "T" ? "bg-gray-300 border-gray-500" : "border-gray-300"
          }`}
          onClick={() => setSelected("T")}
        >
          사고형 (T)
        </button>
      </div>
      <button
        onClick={handleNext}
        disabled={!selected}
        className="mt-8 bg-indigo-500 text-white px-6 py-3 rounded-lg disabled:opacity-40"
      >
        다음
      </button>
    </div>
  );
}
import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function Test() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const type = params.get("type"); // "F" or "T"
  const [answers, setAnswers] = useState([]);
  const questions = [
    "대화 중 감정보다 논리를 더 중요하게 생각한다.",
    "상대의 기분보다 상황의 해결이 더 우선이다.",
    "감정 표현보다는 객관적인 말이 편하다.",
  ];

  const handleAnswer = (value) => {
    const next = [...answers, value];
    setAnswers(next);
    if (next.length === questions.length) {
      const sum = next.reduce((a, b) => a + b, 0);
      const strength = Math.min(4, Math.max(1, Math.ceil(sum / 2))); // 1~4단계
      navigate(`/result?type=${type}&level=${strength}`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-b from-white to-indigo-100">
      <h2 className="text-2xl font-bold mb-6">간단한 테스트</h2>
      {answers.length < questions.length ? (
        <div className="text-center">
          <p className="text-lg mb-4">{questions[answers.length]}</p>
          <div className="flex gap-4 justify-center">
            <button
              className="bg-indigo-400 text-white px-4 py-2 rounded"
              onClick={() => handleAnswer(1)}
            >
              아니다
            </button>
            <button
              className="bg-pink-400 text-white px-4 py-2 rounded"
              onClick={() => handleAnswer(3)}
            >
              그렇다
            </button>
          </div>
        </div>
      ) : (
        <p>결과를 계산 중...</p>
      )}
    </div>
  );
}
import { useSearchParams, useNavigate } from "react-router-dom";
import { characters } from "../data/characters";

export default function Result() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const type = params.get("type");
  const level = parseInt(params.get("level"), 10);

  const charData = characters[type][level - 1];

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-b from-indigo-100 to-white text-center">
      <h2 className="text-3xl font-bold mb-4">당신의 캐릭터는...</h2>
      <div className="bg-white shadow-lg p-6 rounded-xl w-80 border">
        <h3 className="text-2xl font-bold mb-2">{charData.name}</h3>
        <p className="text-gray-600">{charData.description}</p>
      </div>
      <button
        onClick={() => navigate("/")}
        className="mt-8 bg-indigo-500 text-white px-6 py-3 rounded-lg"
      >
        홈으로 돌아가기
      </button>
    </div>
  );
}
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import MBTISelect from "./pages/MBTISelect";
import Test from "./pages/Test";
import Result from "./pages/Result";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/mbti" element={<MBTISelect />} />
        <Route path="/test" element={<Test />} />
        <Route path="/result" element={<Result />} />
      </Routes>
    </BrowserRouter>
  );
}
