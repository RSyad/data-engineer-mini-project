import { useState } from 'react';
import './App.css';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(false);

  // This is for the filter
  const [filters, setFilters] = useState({
    item_category: '',
    year: '',
    month: '',
    day: ''
  });

  // This is for the client-side pagination
  const [page, setPage] = useState(1);
  const pageSize = 10;

  const totalPages = Math.ceil(filteredData.length / pageSize);
  const currentPageData = filteredData.slice((page - 1) * pageSize, page * pageSize);

  const handleChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const handleFilter = () => {
    setLoading(true);
    setPage(1);

    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });

    fetch(`http://127.0.0.1:8000/api/price-data?${params.toString()}`)
      .then(res => res.json())
      .then(json => {
        // console.log('API Response:', json);
        setData(json);
        setFilteredData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching data:', err);
        setLoading(false);
      });
  };

  const handlePrev = () => {
    if (page > 1) setPage(prev => prev - 1);
  };

  const handleNext = () => {
    if (page < totalPages) setPage(prev => prev + 1);
  };

  // This is for building the pie chart
  const pieChartData = (() => {
    if (filteredData.length === 0) return null;

    // Count occurrences per item
    const itemCount = {};
    filteredData.forEach(({ item }) => {
      itemCount[item] = (itemCount[item] || 0) + 1;
    });

    const labels = Object.keys(itemCount);
    const dataValues = Object.values(itemCount);

    return {
      labels,
      datasets: [
        {
          label: 'Item Frequency',
          data: dataValues,
          backgroundColor: labels.map(
            () => `#${Math.floor(Math.random() * 16777215).toString(16)}`
          )
        }
      ]
    };
  })();
  
  // This is to customise the pie chart
  const pieChartOptions = {
    responsive: true,
    plugins: {
      tooltip: {
        enabled: true,
        callbacks: {
          label: function (context) {
            const label = context.label || '';
            const value = context.raw || 0;
            const data = context.dataset.data;
            const total = data.reduce((sum, val) => sum + val, 0);
            const percentage = ((value / total) * 100).toFixed(2);
            return `${label}: ${percentage}% (${value} items)`;
          }
        }
      },
      legend: {
        display: false
      }
    }
  };

  return (
    <div className="App">
      <h1>Price Data Dashboard</h1>

      <div className="filter-container">
        <input
          type="text"
          name="item_category"
          placeholder="Item Category"
          value={filters.item_category}
          onChange={handleChange}
        />
        <input
          type="number"
          name="year"
          placeholder="Year"
          value={filters.year}
          onChange={handleChange}
        />
        <input
          type="number"
          name="month"
          placeholder="Month"
          value={filters.month}
          onChange={handleChange}
        />
        <input
          type="number"
          name="day"
          placeholder="Day"
          value={filters.day}
          onChange={handleChange}
        />
        <button onClick={handleFilter}>Filter</button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : currentPageData.length > 0 ? (
        <>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Premise Code</th>
                <th>Item Code</th>
                <th>Price</th>
                <th>Item</th>
                <th>Unit</th>
                <th>Item Group</th>
                <th>Item Category</th>
              </tr>
            </thead>
            <tbody>
              {currentPageData.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.date}</td>
                  <td>{row.premise_code}</td>
                  <td>{row.item_code}</td>
                  <td>{row.price}</td>
                  <td>{row.item}</td>
                  <td>{row.unit}</td>
                  <td>{row.item_group}</td>
                  <td>{row.item_category}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="pagination">
            <button onClick={handlePrev} disabled={page === 1}>Previous</button>
            <span>Page {page} of {totalPages}</span>
            <button onClick={handleNext} disabled={page === totalPages}>Next</button>
          </div>
        </>
      ) : (
        <p>No data to show. Please apply a filter.</p>
      )}

      {pieChartData && (
        <div style={{ maxWidth: '600px', margin: '2rem auto' }}>
          <h2>Item Distribution</h2>
          <Pie data={pieChartData} options={pieChartOptions} />
        </div>
      )}
    </div>
  );
}

export default App;