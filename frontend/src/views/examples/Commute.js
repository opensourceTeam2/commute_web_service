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
import SimpleFooter from "components/Footers/SimpleFooter.js";

class Commute extends React.Component {
  state = {
    result: null,
  };

  componentDidMount() {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;
  }

  getSettings = () => {
    const loginId = localStorage.getItem("loginId") || "guest";
    const settingsKey = `commuteSettings_${loginId}`;

    return JSON.parse(localStorage.getItem(settingsKey)) || null;
  };

  handleCalculate = async () => {
    const settings = this.getSettings();

    if (!settings) {
      return;
    }

    try {
      const loginId = localStorage.getItem("loginId") || "guest";

      const response = await fetch("http://127.0.0.1:8000/api/commute/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          busStop: settings.busStop,
          busNumber: settings.busNumber,
          classStartTime: settings.classStartTime,
          loginId: loginId,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        alert(result.detail || "통학 계산에 실패했습니다.");
        return;
      }

      this.setState({ result });

      const logsKey = `commuteLogs_${loginId}`;
      const savedLogs = JSON.parse(localStorage.getItem(logsKey)) || [];
      localStorage.setItem(logsKey, JSON.stringify([result, ...savedLogs]));
    } catch (error) {
      console.error(error);
      alert("백엔드 서버와 연결하지 못했습니다. 백엔드가 실행 중인지 확인해주세요.");
    }
  };

  render() {
    const settings = this.getSettings();
    const hasSettings =
      settings &&
      settings.busStop &&
      settings.busNumber &&
      settings.classStartTime;

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
                <Col lg="8">
                  <Card className="bg-secondary shadow border-0">
                    <CardBody className="px-lg-5 py-lg-5">
                      <div className="text-center mb-4">
                        <h3 className="font-weight-bold">통학 도우미 실행</h3>
                        <p className="text-muted">
                          설정한 통학 정보를 기준으로 버스 도착 예정 시간과
                          지각 확률을 계산합니다.
                        </p>
                      </div>

                      {!hasSettings ? (
                        <div className="text-center">
                          <p>
                            통학 도우미를 실행하려면 먼저 설정 페이지에서
                            정류장, 버스 번호, 수업 시작 시간을 입력해야 합니다.
                          </p>

                          <Button color="primary" tag={Link} to="/settings">
                            설정하러 가기
                          </Button>
                        </div>
                      ) : (
                        <>
                          <Row className="mb-4">
                            <Col md="4">
                              <Card className="shadow-sm border-0 mb-3">
                                <CardBody>
                                  <small className="text-muted">정류장</small>
                                  <h5 className="mb-0">{settings.busStop}</h5>
                                </CardBody>
                              </Card>
                            </Col>

                            <Col md="4">
                              <Card className="shadow-sm border-0 mb-3">
                                <CardBody>
                                  <small className="text-muted">버스 번호</small>
                                  <h5 className="mb-0">{settings.busNumber}</h5>
                                </CardBody>
                              </Card>
                            </Col>

                            <Col md="4">
                              <Card className="shadow-sm border-0 mb-3">
                                <CardBody>
                                  <small className="text-muted">
                                    수업 시작 시간
                                  </small>
                                  <h5 className="mb-0">
                                    {settings.classStartTime}
                                  </h5>
                                </CardBody>
                              </Card>
                            </Col>
                          </Row>

                          <div className="text-center">
                            <Button
                              color="primary"
                              onClick={this.handleCalculate}
                            >
                              결과 계산하기
                            </Button>
                          </div>

                          {this.state.result && (
                            <Card className="shadow mt-4">
                              <CardBody>
                                <h4 className="font-weight-bold mb-3">
                                  조회 결과
                                </h4>

                                <p>
                                  <strong>버스 도착 예정 시간:</strong> 약{" "}
                                  {this.state.result.arrivalMinutes}분 후
                                </p>

                                <p>
                                  <strong>지각 확률:</strong>{" "}
                                  {this.state.result.lateProbability}%
                                </p>

                                <p>
                                  <strong>안내 문구:</strong>{" "}
                                  {this.state.result.statusMessage}
                                </p>

                                <p className="text-muted mb-0">
                                  조회 시간: {this.state.result.checkedAt}
                                </p>
                              </CardBody>
                            </Card>
                          )}
                        </>
                      )}
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

export default Commute;