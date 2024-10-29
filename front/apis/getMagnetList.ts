export const getMagnetList = async (page: number) => {
    const apiHost = process.env.NEXT_PUBLIC_API_HOST;
    try {
        const response = await fetch(`${apiHost}/points/magnet_t1/leaderboard?page_index=${page}&page_size=10`, { method: 'GET', cache: 'no-cache' });
        if (response.ok && response.status === 200) {
            const data = await response.json();
            return data;
        } else {
            return {
                leaderboard: [],
                total_users: 0
            }
        }
    } catch (error) {
        console.error('getArdioList error', error);
        return {
            leaderboard: [],
            total_users: 0
        }
    }
}