'use client';
import { Footer } from "@/components/Footer";
import Header from "@/components/Header";
import { Main } from "@/components/Main";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-start min-h-screen h-screen w-full bg-customBg bg-cover bg-center bg-no-repeat bg-[#f5f3ff] overflow-y-auto">
      <Header />
      <Main />
      <Footer />
    </div>
  );
}
