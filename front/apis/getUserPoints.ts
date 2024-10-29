export const getUserPoints = async (address: string) => {
    const apiHost = process.env.NEXT_PUBLIC_API_HOST;
    try {
        const response = await fetch(`${apiHost}/points/get_user_points?user_id=${address}`, { method: 'GET', cache: 'no-cache' });
        if (response.ok && response.status === 200) {
            const data = await response.json();
            return data;
        } else {
            throw new Error('getUserPoints error');
        }
    } catch (error) {
        console.error('getUserPoints error', error);
        throw new Error('getUserPoints error');
    }
}