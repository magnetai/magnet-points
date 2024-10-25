import SvgIcon from "./common/SvgIcon";

export function Footer() {
    return (
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
    )
}