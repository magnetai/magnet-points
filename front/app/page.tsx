'use client';
import { Footer } from "@/components/Footer";
import Header from "@/components/Header";
import SearchInput from "@/components/SearchInput";
import { useState } from "react";

export default function Home() {
  const [keyword, setKeyword] = useState("");

  const handleSearch = (keyword: string) => {
    setKeyword(keyword);
  }
  return (
    <div className="flex flex-col items-center justify-start min-h-screen h-screen w-full bg-custom-bg bg-cover bg-center bg-no-repeat bg-[#f5f3ff] overflow-y-auto">
      <Header />
      <main className="flex flex-col items-center flex-1 mt-10 min-w-[854px]">
        <div className="w-full px-[86px] flex">
          <SearchInput keyword={keyword} handleSearch={handleSearch} />
        </div>
      </main>
      <Footer />
    </div>
  );
}
