/*!
=========================================================
* Argon Design System React - v1.1.2
=========================================================
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

class Register extends React.Component {
  state = {
    loginId: "",
    nickname: "",
    password: "",
    passwordConfirm: "",
    errorMessage: "",
    successMessage: "",
  };

  componentDidMount() {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;
  }

  handleRegister = async (event) => {
    event.preventDefault();

    if (
      this.state.loginId.trim() === "" ||
      this.state.password.trim() === ""
    ) {
      this.setState({
        errorMessage: "아이디와 비밀번호를 입력해주세요.",
        successMessage: "",
      });

      return;
    }

    if (this.state.password !== this.state.passwordConfirm) {
      this.setState({
        errorMessage: "비밀번호가 서로 다릅니다.",
        successMessage: "",
      });

      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          loginId: this.state.loginId.trim(),
          nickname: this.state.nickname.trim(),
          password: this.state.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        this.setState({
          errorMessage: data.detail || "회원가입에 실패했습니다.",
          successMessage: "",
        });

        return;
      }

      this.setState({
        errorMessage: "",
        successMessage: "회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.",
      });

      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
    } catch (error) {
      console.error(error);

      this.setState({
        errorMessage: "백엔드 서버와 연결하지 못했습니다.",
        successMessage: "",
      });
    }
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
                        <small>회원가입</small>
                      </div>

                      <div className="text-center mb-4">
                        <h4>통학 도우미 회원가입</h4>
                        <p className="text-muted">
                          회원가입 후 포인트, 뱃지, 테마 정보를 저장할 수 있습니다.
                        </p>
                      </div>

                      <Form role="form" onSubmit={this.handleRegister}>
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
                                this.setState({
                                  loginId: e.target.value,
                                })
                              }
                            />
                          </InputGroup>
                        </FormGroup>

                        <FormGroup className="mb-3">
                          <InputGroup className="input-group-alternative">
                            <InputGroupAddon addonType="prepend">
                              <InputGroupText>
                                <i className="ni ni-hat-3" />
                              </InputGroupText>
                            </InputGroupAddon>

                            <Input
                              placeholder="닉네임"
                              type="text"
                              value={this.state.nickname}
                              onChange={(e) =>
                                this.setState({
                                  nickname: e.target.value,
                                })
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
                              value={this.state.password}
                              onChange={(e) =>
                                this.setState({
                                  password: e.target.value,
                                })
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
                              placeholder="비밀번호 확인"
                              type="password"
                              value={this.state.passwordConfirm}
                              onChange={(e) =>
                                this.setState({
                                  passwordConfirm: e.target.value,
                                })
                              }
                            />
                          </InputGroup>
                        </FormGroup>

                        {this.state.errorMessage && (
                          <div className="text-danger text-center mb-3">
                            {this.state.errorMessage}
                          </div>
                        )}

                        {this.state.successMessage && (
                          <div className="text-success text-center mb-3">
                            {this.state.successMessage}
                          </div>
                        )}

                        <div className="text-center">
                          <Button
                            className="my-4"
                            color="primary"
                            type="submit"
                          >
                            회원가입
                          </Button>
                        </div>

                        <div className="text-center">
                          <Button
                            color="secondary"
                            type="button"
                            onClick={() => {
                              window.location.href = "/login";
                            }}
                          >
                            로그인으로 이동
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

export default Register;