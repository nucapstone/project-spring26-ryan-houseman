import { useEffect, useState } from "react";

export default function HospitalDetail({changeView, facility_id}) {
  const [facility, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
      const facility_url = `http://127.0.0.1:5000/api/hospitals/${encodeURIComponent(facility_id)}`;
      fetch(facility_url)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((json) => {
          setData(json);
          setLoading(false);
        })
        .catch((err) => {
          setError(err.message);
          setLoading(false);
        });
    }, [facility_id]);
  
    if (loading) return <p>Loading data...</p>;
    if (error) return <p style={{ color: "red" }}>Error: {error}</p>;


  return (
    <div>
      <h2>Hospital Detail</h2>
      <button onClick={() => changeView("search")}>Return to Search</button>
      <p><strong>Facility ID:</strong> {facility.facility_id}</p>
      <p><strong>Facility Name:</strong> {facility.facility_name}</p>
      <p><strong>Address:</strong> {facility.address}</p>
      <p><strong>City/Town:</strong> {facility.citytown}</p>
      <p><strong>State:</strong> {facility.state}</p>
      <p><strong>Zip Code:</strong> {facility.zip_code}</p>
      <p><strong>Hospital Type:</strong> {facility.hospital_type}</p>
      <p><strong>Hospital Rating:</strong> {facility.hospital_overall_rating}</p>
    </div>
  );
}