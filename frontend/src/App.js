import React, { useEffect, useState } from "react";

/**
 * Main App component that handles delivery management.
 * - Fetches and displays delivery records
 * - Allows adding new deliveries
 * - Calculates total delivery cost
 */
function App() {
  const [deliveries, setDeliveries] = useState([]);
  const [totalCost, setTotalCost] = useState(0);
  const [formData, setFormData] = useState({
    driver_id: "",
    start_time: "",
    end_time: "",
    hourly_rate: ""
  });
  const [message, setMessage] = useState("");

  const API_BASE = "http://127.0.0.1:5000";

  useEffect(() => {
    fetchDeliveries();
    fetchTotalCost();
  }, []);

  const fetchDeliveries = async () => {
    try {
      const res = await fetch(`${API_BASE}/deliveries`);
      if (!res.ok) throw new Error("Failed to load deliveries");
      const data = await res.json();
      setDeliveries(data);
    } catch (err) {
      console.error("Error fetching deliveries:", err);
    }
  };

  const fetchTotalCost = async () => {
    try {
      const res = await fetch(`${API_BASE}/total-cost`);
      if (!res.ok) throw new Error("Failed to load total cost");
      const data = await res.json();
      setTotalCost(data.total_cost);
    } catch (err) {
      console.error("Error fetching total cost:", err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    const payload = {
      driver_id: Number(formData.driver_id),
      start_time: formData.start_time,
      end_time: formData.end_time,
      hourly_rate: Number(formData.hourly_rate)
    };

    try {
      const res = await fetch(`${API_BASE}/deliveries`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setMessage("✅ Delivery added!");
        setFormData({ driver_id: "", start_time: "", end_time: "", hourly_rate: "" });
        fetchDeliveries();
        fetchTotalCost();
      } else {
        const errData = await res.json();
        setMessage(`❌ Failed to add delivery: ${errData.message || "Unknown error"}`);
      }
    } catch (err) {
      console.error("Submission error:", err);
      setMessage("❌ Error adding delivery. Please try again.");
    }
  };

  return (
    <div style={styles.container}>
      <h1>📦 Delivery Dashboard</h1>
      <h2>Total Cost: <span style={styles.highlight}>${totalCost.toFixed(2)}</span></h2>

      <section style={styles.section}>
        <h3>Add Delivery</h3>
        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="number"
            name="driver_id"
            placeholder="Driver ID"
            value={formData.driver_id}
            onChange={handleInputChange}
            required
            style={styles.input}
          />
          <input
            type="datetime-local"
            name="start_time"
            value={formData.start_time}
            onChange={handleInputChange}
            required
            style={styles.input}
          />
          <input
            type="datetime-local"
            name="end_time"
            value={formData.end_time}
            onChange={handleInputChange}
            required
            style={styles.input}
          />
          <input
            type="number"
            step="0.01"
            name="hourly_rate"
            placeholder="Hourly Rate"
            value={formData.hourly_rate}
            onChange={handleInputChange}
            required
            style={styles.input}
          />
          <button type="submit" style={styles.button}>Add</button>
        </form>
        {message && <p style={styles.message}>{message}</p>}
      </section>

      <section style={styles.section}>
        <h3>All Deliveries</h3>
        <table style={styles.table}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Driver ID</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Hourly Rate</th>
            </tr>
          </thead>
          <tbody>
            {deliveries.length > 0 ? (
              deliveries.map((d) => (
                <tr key={d.id}>
                  <td>{d.id}</td>
                  <td>{d.driver_id}</td>
                  <td>{new Date(d.start_time).toLocaleString()}</td>
                  <td>{new Date(d.end_time).toLocaleString()}</td>
                  <td>${d.hourly_rate.toFixed(2)}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" style={{ textAlign: "center" }}>No deliveries yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </div>
  );
}

// Inline styling object
const styles = {
  container: {
    maxWidth: "700px",
    margin: "40px auto",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    lineHeight: "1.5"
  },
  section: {
    marginTop: "30px"
  },
  form: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px",
    marginBottom: "15px"
  },
  input: {
    flex: "1 1 120px",
    padding: "6px",
    fontSize: "14px"
  },
  button: {
    padding: "6px 14px",
    fontSize: "14px",
    cursor: "pointer",
    backgroundColor: "#28a745",
    color: "#fff",
    border: "none",
    borderRadius: "4px"
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    border: "1px solid #ccc"
  },
  highlight: {
    color: "#007BFF"
  },
  message: {
    marginTop: "10px",
    fontWeight: "bold"
  }
};

export default App;
