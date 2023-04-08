const axios = require('axios');
const { useState, useEffect } = require('react');
const { Line } = require('react-chartjs-2');
const { connect } = require('react-redux');
const { fetchForexData } = require('./actions/forexActions');

function ForexDisplay(props) {
  const [forexData, setForexData] = useState([]);
  const [searchInput, setSearchInput] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  
  useEffect(() => {
    props.fetchForexData(page, searchInput)
      .then(response => {
        setForexData(response.forexData);
        setTotalPages(response.totalPages);
      });
  }, [page, searchInput]);

  function handleInputChange(event) {
    setSearchInput(event.target.value);
    setPage(1);
  }

  function handlePreviousPageClick() {
    setPage(page - 1);
  }

  function handleNextPageClick() {
    setPage(page + 1);
  }

  const data = {
    labels: forexData.map(data => data.date),
    datasets: [
      {
        label: 'Forex Price',
        data: forexData.map(data => data.price),
        fill: false,
        backgroundColor: '#0066cc',
        borderColor: '#0066cc',
      },
    ],
  };

  const options = {
    scales: {
      xAxes: [
        {
          ticks: {
            autoSkip: true,
            maxTicksLimit: 20,
          },
        },
      ],
    },
  };

  return (
    <div>
      <h1>Forex Prices</h1>
      <form>
        <label htmlFor="searchInput">Search:</label>
        <input id="searchInput" type="text" value={searchInput} onChange={handleInputChange} />
      </form>
      {forexData.length > 0 &&
        <div>
          <Line data={data} options={options} />
          <button onClick={handlePreviousPageClick} disabled={page === 1}>Previous Page</button>
          <button onClick={handleNextPageClick} disabled={page === totalPages}>Next Page</button>
        </div>
      }
      {forexData.length === 0 &&
        <p>Loading...</p>
      }
    </div>
  );
}

const mapDispatchToProps = {
  fetchForexData,
};

export default connect(null, mapDispatchToProps)(ForexDisplay);

##JOB_COMPLETE##