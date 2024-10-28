export const getArdioList = async (page: number) => {
    const apiHost = process.env.NEXT_PUBLIC_API_HOST;
    try {
        const response = await fetch(`${apiHost}/points/ardio_alpha/leaderboard?page_index=${page}&page_size=10`, { method: 'GET', cache: 'no-cache' });
        if (response.ok && response.status === 200) {
            const data = await response.json();
            console.log('ardio data', data);
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