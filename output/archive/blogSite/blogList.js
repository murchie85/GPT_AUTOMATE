import React, { Component } from 'react';
import axios from 'axios';
import BlogCard from './blogCard';

class BlogList extends Component {
  state = {
    blogList: [],
    loading: true,
    error: null,
    currentPage: 1,
    blogsPerPage: 10,
    keyword: '',
    searchFilter: false,
  };

  componentDidMount() {
    this.fetchBlogList();
  }

  fetchBlogList = () => {
    axios
      .get('/api/blog/')
      .then((response) => {
        const blogList = response.data;
        this.setState({ blogList, loading: false });
      })
      .catch((error) => {
        this.setState({ error, loading: false });
      });
  };

  handlePageChange = (pageNumber) => {
    this.setState({ currentPage: pageNumber });
  };

  handleKeywordChange = (event) => {
    const keyword = event.target.value;
    this.setState({ keyword });
  };

  handleSearchFilterChange = () => {
    const { searchFilter } = this.state;
    this.setState({ searchFilter: !searchFilter });
  };

  render() {
    const { blogList, loading, error, currentPage, blogsPerPage, keyword, searchFilter } = this.state;

    const indexOfLastBlog = currentPage * blogsPerPage;
    const indexOfFirstBlog = indexOfLastBlog - blogsPerPage;
    const currentBlogs = blogList.slice(indexOfFirstBlog, indexOfLastBlog);

    const filteredBlogs = currentBlogs.filter((blog) =>
      blog.title.toLowerCase().includes(keyword.toLowerCase())
    );

    const totalBlogs = searchFilter ? filteredBlogs.length : blogList.length;
    const totalPages = Math.ceil(totalBlogs / blogsPerPage);

    const renderBlogCards = loading ? (
      <p>Loading...</p>
    ) : error ? (
      <p>{error.message}</p>
    ) : filteredBlogs.length ? (
      filteredBlogs.map((blog) => <BlogCard key={blog.id} blog={blog} />)
    ) : (
      <p>No blogs found.</p>
    );

    const renderPageNumbers = Array.from({ length: totalPages }, (_, index) => index + 1).map((pageNumber) => (
      <li className={`page-item ${currentPage === pageNumber ? 'active' : ''}`} key={pageNumber}>
        <button type="button" className="page-link" onClick={() => this.handlePageChange(pageNumber)}>
          {pageNumber}
        </button>
      </li>
    ));

    return (
      <div className="container">
        <div className="row">
          <div className="col">
            <div className="my-4 d-flex justify-content-between align-items-center">
              <h2 className="font-weight-bold">Latest Blogs</h2>
              <div className="form-inline">
                <div className="input-group mb-3">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Search by keyword"
                    aria-label="Search by keyword"
                    aria-describedby="basic-addon2"
                    value={keyword}
                    onChange={this.handleKeywordChange}
                  />
                  <div className="input-group-append">
                    <button
                      className={`btn btn-outline-secondary ${searchFilter ? 'active' : ''}`}
                      type="button"
                      onClick={this.handleSearchFilterChange}
                    >
                      Search
                    </button>
                  </div>
                </div>
              </div>
            </div>
            {renderBlogCards}
            <nav aria-label="Blog navigation">
              <ul className="pagination justify-content-end">
                {renderPageNumbers}
              </ul>
            </nav>
          </div>
        </div>
      </div>
    );
  }
}

export default BlogList;##JOB_COMPLETE##