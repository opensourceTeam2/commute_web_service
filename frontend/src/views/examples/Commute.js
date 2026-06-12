import React from "react";
import {
  Button,
  Card,
  CardBody,
  Container,
  Row,
  Col,
  Form,
  FormGroup,
  Label,
  Input,
  Spinner,
} from "reactstrap";

import DemoNavbar from "components/Navbars/DemoNavbar.js";
import SimpleFooter from "components/Footers/SimpleFooter.js";

class Commute extends React.Component {
  state = {
    startLocation: "",
    classStartPeriod: "오전",
    classStartClock: "",
    result: null,
    loading: false,
  };

  componentDidMount() {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;
  }

  getTimeOptions = () => {
    const times = [];

    for (let hour = 1; hour <= 12; hour++) {
      const paddedHour = String(hour).padStart(2, "0");
      times.push(`${paddedHour}:00`);
      times.push(`${paddedHour}:30`);
    }

    return times;
  };

  handleCalculate = async (event) => {
    event.preventDefault();

    const { startLocation, classStartPeriod, classStartClock } = this.state;

    if (
      startLocation.trim() === "" ||
      classStartPeriod.trim() === "" ||
      classStartClock.trim() === ""
    ) {
      alert("출발 위치와 수업 시작 시간을 모두 입력해주세요.");
      return;
    }

    const classStartTime = `${classStartPeriod} ${classStartClock}`;
    const loginId = localStorage.getItem("loginId") || "guest";

    this.setState({ loading: true, result: null });

    try {
      const response = await fetch("http://127.0.0.1:8000/api/commute/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          startLocation: startLocation,
          classStartTime: classStartTime,
          loginId: loginId,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        alert(result.detail || "통학 계산에 실패했습니다.");
        this.setState({ loading: false });
        return;
      }

      this.setState({
        result: result,
        loading: false,
      });

      const logsKey = `commuteLogs_${loginId}`;
      const savedLogs = JSON.parse(localStorage.getItem(logsKey)) || [];
      localStorage.setItem(logsKey, JSON.stringify([result, ...savedLogs]));
    } catch (error) {
      console.error(error);
      alert("백엔드 서버와 연결하지 못했습니다. 백엔드가 실행 중인지 확인해주세요.");
      this.setState({ loading: false });
    }
  };

  renderRouteCard = (route) => {
    return (
      <Card className="shadow mb-4" key={route.rank}>
        <CardBody>
          <h4 className="mb-3">
            추천 경로 {route.rank}
          </h4>

          <p className="mb-2">
            <strong>경로:</strong> {route.routeSummary}
          </p>

          <p className="mb-2">
            <strong>예상 소요 시간:</strong> {route.totalMinutes}분
          </p>

          <p className="mb-2">
            <strong>예상 도착 시간:</strong> {route.expectedArrivalTime}
          </p>

          <p className="mb-2">
            <strong>환승 횟수:</strong> {route.transferCount}회
          </p>

          <p className="mb-2">
            <strong>지각 확률:</strong> {route.lateProbability}%
          </p>

          <p className="mb-3">
            <strong>안내:</strong> {route.statusMessage}
          </p>

          {route.guideMessages && route.guideMessages.length > 0 && (
            <p className="mb-3">
              <strong>날씨 안내:</strong> {route.guideMessages.join(" ")}
            </p>
          )}

          <hr />

          <h6>상세 이동 순서</h6>
          <ol>
            {route.steps.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ol>

          {route.reasons && route.reasons.length > 0 && (
            <>
              <h6>계산 이유</h6>
              <ul>
                {route.reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </>
          )}
        </CardBody>
      </Card>
    );
  };

  render() {
    const timeOptions = this.getTimeOptions();
    const { result, loading } = this.state;

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
                      <h3 className="mb-4">통학 도우미 실행</h3>

                      <p>
                        출발 위치와 수업 시작 시간을 입력하면 단국대학교까지 갈 수 있는
                        경로 중 지각 확률이 낮은 3가지를 추천합니다.
                      </p>

                      <Form onSubmit={this.handleCalculate}>
                        <FormGroup>
                          <Label>출발 위치</Label>
                          <Input
                            type="text"
                            placeholder="예: 미금역, 죽전역, 수지구청역, 강남역"
                            value={this.state.startLocation}
                            onChange={(e) =>
                              this.setState({ startLocation: e.target.value })
                            }
                          />
                        </FormGroup>

                        <FormGroup>
                          <Label>수업 시작 시간</Label>
                          <Row>
                            <Col md="4">
                              <Input
                                type="select"
                                value={this.state.classStartPeriod}
                                onChange={(e) =>
                                  this.setState({
                                    classStartPeriod: e.target.value,
                                  })
                                }
                              >
                                <option value="오전">오전</option>
                                <option value="오후">오후</option>
                              </Input>
                            </Col>

                            <Col md="8">
                              <Input
                                type="select"
                                value={this.state.classStartClock}
                                onChange={(e) =>
                                  this.setState({
                                    classStartClock: e.target.value,
                                  })
                                }
                              >
                                <option value="">시간을 선택하세요</option>
                                {timeOptions.map((time) => (
                                  <option key={time} value={time}>
                                    {time}
                                  </option>
                                ))}
                              </Input>
                            </Col>
                          </Row>
                        </FormGroup>

                        <Button color="primary" type="submit" disabled={loading}>
                          {loading ? (
                            <>
                              <Spinner size="sm" /> 계산 중...
                            </>
                          ) : (
                            "경로 추천받기"
                          )}
                        </Button>
                      </Form>
                    </CardBody>
                  </Card>

                  {result && (
                    <div className="mt-5">
                      <h3 className="text-white mb-4">추천 결과</h3>

                      <Card className="shadow mb-4">
                        <CardBody>
                          <p>
                            <strong>출발 위치:</strong> {result.startLocation}
                          </p>
                          <p>
                            <strong>도착지:</strong> {result.destination}
                          </p>
                          <p>
                            <strong>수업 시작 시간:</strong>{" "}
                            {result.classStartTime}
                          </p>
                          <p>
                            <strong>조회 시간:</strong> {result.checkedAt}
                          </p>
                        </CardBody>
                      </Card>

                      {result.routes.map((route) => this.renderRouteCard(route))}
                    </div>
                  )}
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