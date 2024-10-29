'use client';
import { useEffect, useState } from "react";
import SearchInput from "./SearchInput";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "./ui/pagination";
import { getArdioList } from "@/apis/getArdioList";
import { getMagnetList } from "@/apis/getMagnetList";
import { getUserPoints } from "@/apis/getUserPoints";
import { Skeleton } from "./ui/skeleton";

const tableTypes = ["Ardio Alpha", "Magnet T1"];

interface RankItem {
    user_id: string;
    points: number;
    rank: number;
}

interface SearchItem {
    user_id: string;
    ardio_alpha_points: number;
    t1_points: number;
}


export function Main() {
    const [keyword, setKeyword] = useState("");
    const [tableType, setTableType] = useState(tableTypes[0]);
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [rankList, setRankList] = useState<RankItem[]>([]);
    const [searchList, setSearchList] = useState<SearchItem[]>([]);
    const [showSearchList, setShowSearchList] = useState(false);
    const [activePagenationArray, setActivePagenationArray] = useState<number[]>([])
    const [totalPage, setTotalPage] = useState(1);
    const [pagenationArray, setPagenationArray] = useState<number[]>([]);

    const handleSearch = (keyword: string) => {
        const realKeyword = keyword.trim();
        setKeyword(realKeyword);
    }

    const handleTypeChange = async (type: string) => {
        setTableType(type);
        setKeyword("");
        setCurrentPage(1);
    }

    useEffect(() => {
        hanleDataFetch();
    }, [keyword, currentPage, tableType])

    useEffect(() => {
        const pagenationArray = Array.from({ length: Math.ceil(Number(totalPage) / 10) }, (_, i) => i + 1)
        if (pagenationArray.length > 3) {
            setActivePagenationArray(pagenationArray.slice(0, 3))
        } else {
            setActivePagenationArray(pagenationArray)
        }
        setPagenationArray(pagenationArray);
    }, [totalPage])



    const hanleDataFetch = async () => {
        const len = keyword.length;
        if (len === 0) {
            setLoading(true);
            const list = await handleGetList(currentPage, tableType);
            setRankList(list.leaderboard);
            setTotalPage(list.total_users);
            setShowSearchList(false);
            setLoading(false);
        } else if (len > 0 && len < 42) {
            return;
        } else if (len === 42) {
            setLoading(true);
            const { user_id, ardio_alpha_points, t1_points } = await getUserPoints(keyword);
            setSearchList([{ user_id, ardio_alpha_points, t1_points }]);
            setShowSearchList(true);
            setLoading(false);
        } else {
            return;
        }
    }

    useEffect(() => {
        if (currentPage === 1) {
            setActivePagenationArray(pagenationArray.slice(0, 3))
        } else if (currentPage === pagenationArray.length) {
            setActivePagenationArray(pagenationArray.slice(-3))
        } else {
            setActivePagenationArray(pagenationArray.slice(currentPage - 2, currentPage + 1))
        }
    }, [currentPage])


    const prevPage = async () => {
        if (currentPage === 1) return
        setCurrentPage(currentPage - 1)
    }

    const nextPage = async () => {
        if (currentPage === pagenationArray.length) return
        setCurrentPage(currentPage + 1)
    }

    const handleGetList = async (page: number, type: string) => {
        switch (type) {
            case "Ardio Alpha":
                return await getArdioList(page);
            case "Magnet T1":
                return await getMagnetList(page);
            default:
                return await getArdioList(page);
        }
    }



    return (
        <main className="flex flex-col items-center flex-1 mt-10 min-w-[854px]">
            <div className="w-full px-[86px] flex">
                <SearchInput keyword={keyword} handleSearch={handleSearch} />
            </div>
            <div className="w-full mt-8 flex flex-col items-center">
                {
                    !showSearchList && (
                        <Select defaultValue={tableType} onValueChange={handleTypeChange}>
                            <SelectTrigger className="w-[180px] bg-white border-none focus:ring-transparent" value={tableType}>
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                {
                                    tableTypes.map((type) => (
                                        <SelectItem
                                            key={type}
                                            value={type}>
                                            {type}
                                        </SelectItem>
                                    ))
                                }
                            </SelectContent>
                        </Select>
                    )
                }
                <div className="w-full">
                    {

                        loading ? (<Loading currentPage={currentPage} setCurrentPage={setCurrentPage} activePagenationArray={activePagenationArray} prevPage={prevPage} nextPage={nextPage} />) : showSearchList ? (<SearchList list={searchList} />) : (<TableList list={rankList} currentPage={currentPage} setCurrentPage={setCurrentPage} activePagenationArray={activePagenationArray} prevPage={prevPage} nextPage={nextPage} />)
                    }
                </div>
            </div>
        </main>
    )
}

function Loading({ currentPage, setCurrentPage, activePagenationArray, prevPage, nextPage }: { currentPage: number, activePagenationArray: number[], prevPage: () => void, nextPage: () => void, setCurrentPage: (page: number) => void }) {
    return (
        <div className="w-full flex flex-col items-center">
            <div className="w-full flex flex-col bg-[#FFFFFF99] opacity-60 rounded-[20px] py-5 mt-4">
                <div className="grid grid-cols-3 gap-40 text-center border-b-[1px] border-[#EBEBEB] pb-[14px] px-[150px]">
                    <Skeleton className="w-[60px] h-[24px] col-span-1" />
                    <Skeleton className="w-[44px] h-[24px] col-span-1" />
                    <Skeleton className="w-[36px] h-[24px] col-span-1" />
                </div>
                <div className="mt-4 flex flex-col gap-8">
                    {
                        Array.from({ length: 10 }, (_, index) => (
                            <div key={index} className="grid grid-cols-3 gap-40 text-center px-[150px]">
                                <Skeleton className="w-[106px] h-[24px] col-span-1" />
                                <Skeleton className="w-[40px] h-[24px] col-span-1" />
                                <Skeleton className="w-[20px] h-[24px] col-span-1" />
                            </div>
                        ))
                    }
                </div>
            </div>
            <div className="mt-6">
                <Pagination>
                    <PaginationContent>
                        <PaginationItem>
                            <PaginationPrevious className="cursor-pointer" onClick={prevPage} />
                        </PaginationItem>
                        {
                            activePagenationArray.map((page, index) => (
                                <PaginationItem key={index} onClick={() => { setCurrentPage(page) }}>
                                    <PaginationLink className="cursor-pointer" isActive={currentPage === page}>{page}</PaginationLink>
                                </PaginationItem>
                            ))
                        }
                        <PaginationItem>
                            <PaginationNext className="cursor-pointer" onClick={nextPage} />
                        </PaginationItem>
                    </PaginationContent>
                </Pagination>
            </div>
        </div>
    )

}

function SearchList({ list }: { list: SearchItem[] }) {
    return (
        <div className="w-full flex flex-col items-center">
            <div className="w-full flex flex-col bg-[#FFFFFF99] opacity-60 rounded-[20px] py-5 mt-4">
                <div className="grid grid-cols-3 gap-40 border-b-[1px] border-[#EBEBEB] pb-[14px] pl-[141px] pr-[139px]">
                    <span className="col-span-1">Address</span>
                    <span className="col-span-1">Ardio Alpha Points</span>
                    <span className="col-span-1">Magnet T1 Points</span>
                </div>
                <div className="mt-4 flex flex-col gap-8">
                    {
                        list.map((item, index) => (
                            <div key={index} className="grid grid-cols-3 gap-40 text-center pl-[115px] pr-[150px]">
                                <span className="col-span-1">{item.user_id}</span>
                                <span className="col-span-1">{item.ardio_alpha_points}</span>
                                <span className="col-span-1">{item.t1_points}</span>
                            </div>
                        ))
                    }
                </div>
            </div>
        </div>
    )
}


function TableList({ list, currentPage, setCurrentPage, activePagenationArray, prevPage, nextPage, }: { list: RankItem[], currentPage: number, activePagenationArray: number[], prevPage: () => void, nextPage: () => void, setCurrentPage: (page: number) => void }) {
    return (
        <div className="w-full flex flex-col items-center">
            <div className="w-full flex flex-col bg-[#FFFFFF99] opacity-60 rounded-[20px] py-5 mt-4">
                <div className="grid grid-cols-3 gap-40 text-center border-b-[1px] border-[#EBEBEB] pb-[14px] px-[150px]">
                    <span className="col-span-1">Address</span>
                    <span className="col-span-1">Points</span>
                    <span className="col-span-1">Rank</span>
                </div>
                <div className="mt-4 flex flex-col gap-8">
                    {
                        list.map((item, index) => (
                            <div key={index} className="grid grid-cols-3 gap-40 text-center px-[150px]">
                                <span className="col-span-1">{item.user_id}</span>
                                <span className="col-span-1">{item.points}</span>
                                <span className="col-span-1">{item.rank}</span>
                            </div>
                        ))
                    }
                </div>
            </div>
            <div className="mt-6">
                <Pagination>
                    <PaginationContent>
                        <PaginationItem>
                            <PaginationPrevious className="cursor-pointer" onClick={prevPage} />
                        </PaginationItem>
                        {
                            activePagenationArray.map((page, index) => (
                                <PaginationItem key={index} onClick={() => { setCurrentPage(page) }}>
                                    <PaginationLink className="cursor-pointer" isActive={currentPage === page}>{page}</PaginationLink>
                                </PaginationItem>
                            ))
                        }
                        <PaginationItem>
                            <PaginationNext className="cursor-pointer" onClick={nextPage} />
                        </PaginationItem>
                    </PaginationContent>
                </Pagination>
            </div>
        </div>
    )
}