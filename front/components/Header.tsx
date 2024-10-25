import SvgIcon from "./common/SvgIcon";

export function Header() {
    return (
        <header className="mt-28 flex flex-col items-center max-w-[684px]">
            <SvgIcon name="title" width={404} height={44} />
            <div className="flex flex-col items-start mt-8 text-base break-words text-[#666]">
                <p>Magnet Points are a way to recognize and reward your contributions within the Magnet</p>
                <p>Labs community. Earn points by engaging with our platform, completing tasks, and</p>
                <p>participating in events. The more you contribute, the higher you climb on the leaderboard!</p>
            </div>
        </header>
    )
}

export default Header;