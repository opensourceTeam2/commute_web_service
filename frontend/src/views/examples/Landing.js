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

import {
  Button,
  Card,
  CardBody,
  Container,
  Row,
  Col,
} from "reactstrap";

import DemoNavbar from "components/Navbars/DemoNavbar.js";
import CardsFooter from "components/Footers/CardsFooter.js";

class Landing extends React.Component {
  componentDidMount() {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;
  }

  render() {
    return (
      <>
        <DemoNavbar />

        <main ref="main">
          <div className="position-relative">
            <section className="section section-lg section-shaped pb-250">
              <div className="shape shape-style-1 shape-default">
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
              </div>

              <Container className="py-lg-md d-flex">
                <div className="col px-0">
                  <Row>
                    <Col lg="7">
                      <h1 className="display-3 text-white">
                        통학 시간을 예측하고
                        <span>지각 확률을 확인하세요</span>
                      </h1>

                      <p className="lead text-white">
                        자주 이용하는 정류장과 버스 번호를 설정하면,
                        버스 도착 예정 시간과 지각 가능성을 한눈에 확인할 수
                        있습니다.
                      </p>

                      <div className="btn-wrapper">
                        <Button
                          className="btn-icon mb-3 mb-sm-0"
                          color="info"
                          tag={Link}
                          to="/commute"
                        >
                          <span className="btn-inner--icon mr-1">
                            <i className="ni ni-bus-front-12" />
                          </span>
                          <span className="btn-inner--text">
                            통학 도우미 실행하기
                          </span>
                        </Button>

                        <Button
                          className="btn-white btn-icon mb-3 mb-sm-0 ml-1"
                          color="default"
                          tag={Link}
                          to="/settings"
                        >
                          <span className="btn-inner--icon mr-1">
                            <i className="ni ni-settings-gear-65" />
                          </span>
                          <span className="btn-inner--text">설정하기</span>
                        </Button>
                      </div>
                    </Col>
                  </Row>
                </div>
              </Container>

              <div className="separator separator-bottom separator-skew">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  preserveAspectRatio="none"
                  version="1.1"
                  viewBox="0 0 2560 100"
                  x="0"
                  y="0"
                >
                  <polygon
                    className="fill-white"
                    points="2560 0 2560 100 0 100"
                  />
                </svg>
              </div>
            </section>
          </div>

          <section className="section section-lg pt-lg-0 mt--200">
            <Container>
              <Row className="justify-content-center">
                <Col lg="12">
                  <Row className="row-grid">
                    <Col lg="4">
                      <Card className="card-lift--hover shadow border-0">
                        <CardBody className="py-5">
                          <div className="icon icon-shape icon-shape-primary rounded-circle mb-4">
                            <i className="ni ni-bus-front-12" />
                          </div>

                          <h6 className="text-primary text-uppercase">
                            버스 도착 예정 시간
                          </h6>

                          <p className="description mt-3">
                            설정한 정류장과 버스 번호를 기준으로 도착 예정
                            시간을 확인할 수 있습니다.
                          </p>
                        </CardBody>
                      </Card>
                    </Col>

                    <Col lg="4">
                      <Card className="card-lift--hover shadow border-0">
                        <CardBody className="py-5">
                          <div className="icon icon-shape icon-shape-success rounded-circle mb-4">
                            <i className="ni ni-watch-time" />
                          </div>

                          <h6 className="text-success text-uppercase">
                            지각 확률 계산
                          </h6>

                          <p className="description mt-3">
                            수업 시작 시간과 예상 도착 정보를 바탕으로 지각
                            가능성을 계산합니다.
                          </p>
                        </CardBody>
                      </Card>
                    </Col>

                    <Col lg="4">
                      <Card className="card-lift--hover shadow border-0">
                        <CardBody className="py-5">
                          <div className="icon icon-shape icon-shape-warning rounded-circle mb-4">
                            <i className="ni ni-single-copy-04" />
                          </div>

                          <h6 className="text-warning text-uppercase">
                            조회 로그 저장
                          </h6>

                          <p className="description mt-3">
                            사용자가 조회한 통학 도우미 결과를 저장하고, 로그
                            페이지에서 다시 확인할 수 있습니다.
                          </p>
                        </CardBody>
                      </Card>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Container>
          </section>

          <section className="section">
            <Container>
              <Row className="justify-content-center text-center mb-lg">
                <Col lg="8">
                  <h2 className="display-3">서비스 이용 흐름</h2>
                  <p className="lead text-muted">
                    로그인 후 설정을 입력하고, 통학 도우미 실행 화면에서 결과를
                    조회하면 됩니다.
                  </p>
                </Col>
              </Row>

              <Row>
                <Col md="4">
                  <Card className="shadow border-0 mb-4">
                    <CardBody>
                      <h5>1. 로그인</h5>
                      <p className="mb-0">
                        아이디와 비밀번호를 입력하여 서비스를 이용합니다.
                      </p>
                    </CardBody>
                  </Card>
                </Col>

                <Col md="4">
                  <Card className="shadow border-0 mb-4">
                    <CardBody>
                      <h5>2. 설정 입력</h5>
                      <p className="mb-0">
                        자주 이용하는 정류장, 버스 번호, 수업 시작 시간을
                        저장합니다.
                      </p>
                    </CardBody>
                  </Card>
                </Col>

                <Col md="4">
                  <Card className="shadow border-0 mb-4">
                    <CardBody>
                      <h5>3. 결과 조회</h5>
                      <p className="mb-0">
                        도착 예정 시간과 지각 확률을 확인하고 로그로 저장합니다.
                      </p>
                    </CardBody>
                  </Card>
                </Col>
              </Row>
            </Container>
          </section>
        </main>

        <CardsFooter />
      </>
    );
  }
}

export default Landing;