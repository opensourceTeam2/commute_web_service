/*!

=========================================================
* Argon Design System React - v1.1.2
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-design-system-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-design-system-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

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
              <NavbarBrand className="mr-lg-5" tag={Link} to="/">
                <span className="text-white font-weight-bold">
                  통학 도우미
                </span>
              </NavbarBrand>

              <button className="navbar-toggler" id="navbar_global">
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
                        <span className="font-weight-bold text-primary">
                          통학 도우미
                        </span>
                      </Link>
                    </div>
                    <div className="col-6 collapse-close">
                      <button className="navbar-toggler" id="navbar_global">
                        <span />
                        <span />
                      </button>
                    </div>
                  </div>
                </div>

                <Nav className="align-items-lg-center ml-lg-auto" navbar>
                  <NavItem>
                    <NavLink tag={Link} to="/commute">
                      통학 도우미 실행
                    </NavLink>
                  </NavItem>

                  <NavItem>
                    <NavLink tag={Link} to="/settings">
                      설정
                    </NavLink>
                  </NavItem>

                  <NavItem>
                    <NavLink tag={Link} to="/logs">
                      로그
                    </NavLink>
                  </NavItem>

                  <NavItem className="d-none d-lg-block ml-lg-4">
                    {!isLoggedIn ? (
                      <Button
                        className="btn-neutral btn-icon"
                        color="default"
                        tag={Link}
                        to="/login"
                      >
                        <span className="btn-inner--icon">
                          <i className="fa fa-user mr-2" />
                        </span>
                        <span className="nav-link-inner--text">로그인</span>
                      </Button>
                    ) : (
                      <Button
                        className="btn-neutral btn-icon"
                        color="default"
                        onClick={this.handleLogout}
                      >
                        <span className="btn-inner--icon">
                          <i className="fa fa-sign-out mr-2" />
                        </span>
                        <span className="nav-link-inner--text">로그아웃</span>
                      </Button>
                    )}
                  </NavItem>
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