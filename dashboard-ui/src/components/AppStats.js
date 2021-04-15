import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://acit3855-sba-microservices-vm-cameron-woolfries.eastus2.cloudapp.azure.com/processing/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Shifts</th>
							<th>Incomes</th>
						</tr>
						<tr>
							<td># Shifts: {stats['num_shifts']}</td>
							<td># Incomes: {stats['num_incomes']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Income: {stats['max_income']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['timestamp']}</h3>

            </div>
        )
    }
}
