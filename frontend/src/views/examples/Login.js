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

import {
  Button,
  Card,
  CardBody,
  FormGroup,
  Form,
  Input,
  InputGroupAddon,
  InputGroupText,
  InputGroup,
  Container,
  Row,
  Col,
} from "reactstrap";

import DemoNavbar from "components/Navbars/DemoNavbar.js";
import SimpleFooter from "components/Footers/SimpleFooter.js";

class Login extends React.Component {
  state = {
    loginId: "",
    password: "",
    errorMessage: "",
  };

  componentDidMount() {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;
  }

  handleLogin = (event) => {
    event.preventDefault();

    if (this.state.loginId.trim() === "" || this.state.password.trim() === "") {
      this.setState({
        errorMessage: "아이디와 비밀번호를 모두 입력해주세요.",
      });
      return;
    }

    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("loginId", this.state.loginId.trim());

    window.location.href = "/commute";
  };

  render() {
    return (
      <>
        <DemoNavbar />

        <main ref="main">
          <section className="section section-shaped section-lg">
            <div className="shape shape-style-1 bg-gradient-default">
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
            </div>

            <Container className="pt-lg-7">
              <Row className="justify-content-center">
                <Col lg="5">
                  <Card className="bg-secondary shadow border-0">
                    <CardBody className="px-lg-5 py-lg-5">
                      <div className="text-center text-muted mb-4">
                        <h4 className="font-weight-bold">로그인</h4>
                        <small>
                          통학 도우미 기능을 이용하려면 로그인이 필요합니다.
                        </small>
                      </div>

                      <Form role="form" onSubmit={this.handleLogin}>
                        <FormGroup className="mb-3">
                          <InputGroup className="input-group-alternative">
                            <InputGroupAddon addonType="prepend">
                              <InputGroupText>
                                <i className="ni ni-single-02" />
                              </InputGroupText>
                            </InputGroupAddon>
                            <Input
                              placeholder="아이디"
                              type="text"
                              value={this.state.loginId}
                              onChange={(e) =>
                                this.setState({ loginId: e.target.value })
                              }
                            />
                          </InputGroup>
                        </FormGroup>

                        <FormGroup>
                          <InputGroup className="input-group-alternative">
                            <InputGroupAddon addonType="prepend">
                              <InputGroupText>
                                <i className="ni ni-lock-circle-open" />
                              </InputGroupText>
                            </InputGroupAddon>
                            <Input
                              placeholder="비밀번호"
                              type="password"
                              autoComplete="off"
                              value={this.state.password}
                              onChange={(e) =>
                                this.setState({ password: e.target.value })
                              }
                            />
                          </InputGroup>
                        </FormGroup>

                        {this.state.errorMessage && (
                          <p className="text-danger text-center mt-3">
                            {this.state.errorMessage}
                          </p>
                        )}

                        <div className="text-center">
                          <Button className="my-4" color="primary" type="submit">
                            로그인
                          </Button>
                        </div>
                      </Form>
                    </CardBody>
                  </Card>
                </Col>
              </Row>
            </Container>
          </section>
        </main>

        <SimpleFooter />
      </>
    );
  }
}

export default Login;