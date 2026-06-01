/*!
=========================================================
* Argon Design System React - v1.1.2
=========================================================
*/

import React from "react";
import { Link } from "react-router-dom";
import Headroom from "headroom.js";

import {
  Button,
  UncontrolledCollapse,
  NavbarBrand,
  Navbar,
  NavItem,
  NavLink,
  Nav,
  Container,
} from "reactstrap";

class DemoNavbar extends React.Component {
  state = {
    collapseClasses: "",
    collapseOpen: false,
  };

  componentDidMount() {
    let headroom = new Headroom(document.getElementById("navbar-main"));
    headroom.init();
  }

  onExiting = () => {
    this.setState({
      collapseClasses: "collapsing-out",
    });
  };

  onExited = () => {
    this.setState({
      collapseClasses: "",
    });
  };

  handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("loginId");
    localStorage.removeItem("nickname");
    localStorage.removeItem("selectedTheme");

    window.location.href = "/login";
  };

  render() {
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

    return (
      <>
        <header className="header-global">
          <Navbar
            className="navbar-main navbar-transparent navbar-light headroom"
            expand="lg"
            id="navbar-main"
          >
            <Container>
              <NavbarBrand
                className="mr-lg-5"
                to="/"
                tag={Link}
              >
                통학 도우미
              </NavbarBrand>

              <button
                className="navbar-toggler"
                id="navbar_global"
              >
                <span className="navbar-toggler-icon" />
              </button>

              <UncontrolledCollapse
                toggler="#navbar_global"
                navbar
                className={this.state.collapseClasses}
                onExiting={this.onExiting}
                onExited={this.onExited}
              >
                <div className="navbar-collapse-header">
                  <div className="row">
                    <div className="col-6 collapse-brand">
                      <Link to="/">
                        통학 도우미
                      </Link>
                    </div>

                    <div className="col-6 collapse-close">
                      <button
                        className="navbar-toggler"
                        id="navbar_global"
                      >
                        <span />
                        <span />
                      </button>
                    </div>
                  </div>
                </div>

                <Nav
                  className="navbar-nav-hover align-items-lg-center"
                  navbar
                >
                  <NavItem>
                    <NavLink
                      to="/commute"
                      tag={Link}
                    >
                      <i className="ni ni-bus-front-12 d-lg-none mr-1" />
                      <span className="nav-link-inner--text">
                        통학 도우미 실행
                      </span>
                    </NavLink>
                  </NavItem>

                  <NavItem>
                    <NavLink
                      to="/logs"
                      tag={Link}
                    >
                      <i className="ni ni-bullet-list-67 d-lg-none mr-1" />
                      <span className="nav-link-inner--text">
                        로그
                      </span>
                    </NavLink>
                  </NavItem>

                  <NavItem>
                    <NavLink
                      to="/badge"
                      tag={Link}
                    >
                      <i className="ni ni-trophy d-lg-none mr-1" />
                      <span className="nav-link-inner--text">
                        포인트 / 뱃지
                      </span>
                    </NavLink>
                  </NavItem>

                  <NavItem>
                    <NavLink
                      to="/theme-shop"
                      tag={Link}
                    >
                      <i className="ni ni-palette d-lg-none mr-1" />
                      <span className="nav-link-inner--text">
                        테마 상점
                      </span>
                    </NavLink>
                  </NavItem>
                </Nav>

                <Nav
                  className="align-items-lg-center ml-lg-auto"
                  navbar
                >
                  {!isLoggedIn ? (
                    <>
                      <NavItem>
                        <Button
                          className="btn-neutral btn-icon"
                          color="default"
                          to="/login"
                          tag={Link}
                        >
                          <span className="btn-inner--icon">
                            <i className="fa fa-sign-in mr-2" />
                          </span>
                          <span className="nav-link-inner--text">
                            로그인
                          </span>
                        </Button>
                      </NavItem>

                      <NavItem className="ml-lg-2">
                        <Button
                          className="btn-neutral btn-icon"
                          color="default"
                          to="/register"
                          tag={Link}
                        >
                          <span className="btn-inner--icon">
                            <i className="fa fa-user-plus mr-2" />
                          </span>
                          <span className="nav-link-inner--text">
                            회원가입
                          </span>
                        </Button>
                      </NavItem>
                    </>
                  ) : (
                    <NavItem>
                      <Button
                        className="btn-neutral btn-icon"
                        color="default"
                        onClick={this.handleLogout}
                      >
                        <span className="btn-inner--icon">
                          <i className="fa fa-sign-out mr-2" />
                        </span>
                        <span className="nav-link-inner--text">
                          로그아웃
                        </span>
                      </Button>
                    </NavItem>
                  )}
                </Nav>
              </UncontrolledCollapse>
            </Container>
          </Navbar>
        </header>
      </>
    );
  }
}

export default DemoNavbar;