import SvgIcon from '@/components/common/SvgIcon'
import React from 'react'

export default function SearchInput({ keyword, handleSearch }: { keyword: string, handleSearch: (keyword: string) => void }) {
    return (
        <div className='flex-1 flex flex-row items-center justify-between outline-[#DEDEDE] outline-1 rounded-xl bg-white pl-2.5 py-2 focus-within:outline-[#DEDEDE] focus-within:outline-2 focus-within:border-none'>
            <SvgIcon
                name='search'
                width={30}
                height={30}
                className='mr-3.5 flex-none'
            />
            <input
                type='text'
                value={keyword}
                onChange={(e) => handleSearch(e.target.value)}
                placeholder='Search for Blockchain address'
                className='flex-1 focus:outline-none'
            />
            {keyword.trim() !== '' &&
                (<div
                    onClick={() => handleSearch('')}
                    className='mx-2 text-[#999] text-sm cursor-pointer'
                >
                    Clear All
                </div>
                )}
        </div>
    )
}
