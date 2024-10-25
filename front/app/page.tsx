'use client';
import SvgIcon from "@/components/common/SvgIcon";
import SearchInput from "@/components/SearchInput";
import { useState } from "react";

export default function Home() {
  const [keyword, setKeyword] = useState("");

  const handleSearch = (keyword: string) => {
    setKeyword(keyword);
  }
  return (
    <div className="flex flex-col items-center justify-start min-h-screen h-screen bg-custom-bg bg-cover bg-center bg-no-repeat bg-[#f5f3ff] overflow-y-scroll">
      <header className="mt-28 flex flex-col items-center max-w-[684px]">
        <SvgIcon name="title" width={404} height={44} />
        <div className="flex flex-col items-start mt-8 text-base break-words text-[#666]">
          <p>Magnet Points are a way to recognize and reward your contributions within the Magnet</p>
          <p>Labs community. Earn points by engaging with our platform, completing tasks, and</p>
          <p>participating in events. The more you contribute, the higher you climb on the leaderboard!</p>
        </div>
      </header>

      <main className="flex flex-col items-center flex-1 mt-10 min-w-[854px]">
        <div className="w-full px-[86px] flex">
          <SearchInput keyword={keyword} handleSearch={handleSearch} />
        </div>

      </main>
      <footer className="flex flex-col items-center justify-center mt-7 max-w-[684px] mb-28">
        <div className="flex flex-col items-start text-[#666] text-base font-medium">
          <p className="leading-6"><span className="text-[#603AF8] font-semibold cursor-pointer">Ardio Alpha </span> is now live!</p>

          <div className="flex flex-col items-start text-base font-medium text-[#666]">
            <p className="leading-6">Join Ardio Alpha, currently live, to boost your Magnet Points. Interact with Ardio Alpha, </p>
            <p className="leading-6">provide feedback, and explore new features to accumulate points while helping us shape </p>
            <p className="leading-6">the future of Ardio, and Action Agents to come!</p>
          </div>

          <p className="leading-6">Keep an eye on your score and see how you rank among fellow community members!</p>
          <p className="leading-6">Every point counts – rise to the top and claim your place on the leaderboard!</p>
        </div>
        <div className="mt-8 flex justify-center">
          <SvgIcon name="footer" width={256} height={36} />
        </div>
      </footer>
    </div>
  );
}
