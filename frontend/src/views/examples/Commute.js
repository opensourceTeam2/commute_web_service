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
    theme:
      localStorage.getItem(
        "selectedTheme"
      ) || "default",
    startLocation: "",
    classStartPeriod: "오전",
    classStartClock: "",
    result: null,
    loading: false,
    showPlaylist: false,
    playlists: [],
    pointResult: null,
    arrivedToday: false,
    arriving: false,
    expandedRouteRanks: {},
  };

  componentDidMount() {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;

    const loginId =
  localStorage.getItem("loginId");

fetch(
  `http://127.0.0.1:8000/themes?login_id=${loginId}`
)
  .then((response) =>
    response.json()
  )
  .then((data) => {

    localStorage.setItem(
      "selectedTheme",
      data?.selected_theme || "default"
    );

    this.setState({
      theme:
        data?.selected_theme || "default"
    });
  });
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

    this.setState({
      loading: true,
      result: null,
      pointResult: null,
      showPlaylist: false,
      playlists: [],
      arrivedToday: false,
      expandedRouteRanks: {},
    });

    try {
      const response = await fetch("http://127.0.0.1:8000/api/commute/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          startLocation,
          classStartTime,
          loginId,
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

    } catch (error) {
      console.error(error);
      alert("백엔드 서버와 연결하지 못했습니다. 백엔드가 실행 중인지 확인해주세요.");
      this.setState({ loading: false });
    }
  };

    toggleRouteDetail = (routeRank) => {
    this.setState((prevState) => ({
      expandedRouteRanks: {
        ...prevState.expandedRouteRanks,
        [routeRank]: !prevState.expandedRouteRanks[routeRank],
      },
    }));
  };

  renderRouteCard = (route) => {
    const routeRank = route.rank;
    const isExpanded = !!this.state.expandedRouteRanks[routeRank];

    const steps = Array.isArray(route.steps) ? route.steps : [];
    const reasons = Array.isArray(route.reasons) ? route.reasons : [];

    return (
      <Card className="shadow mb-4" key={route.rank}>
        <CardBody>
          <Row className="align-items-center">
            <Col md="8">
              <h4>추천 경로 {route.rank}</h4>

              <p>
                <strong>경로:</strong> {route.routeSummary}
              </p>

              <p>
                <strong>예상 소요 시간:</strong> {route.totalMinutes}분
              </p>

              <p className="mb-md-0">
                <strong>지각 확률:</strong> {route.lateProbability}%
              </p>
            </Col>

            <Col md="4" className="text-md-right mt-3 mt-md-0">
              <Button
                color={isExpanded ? "secondary" : "primary"}
                size="sm"
                onClick={() => this.toggleRouteDetail(routeRank)}
              >
                {isExpanded ? "최소화" : "최대화"}
              </Button>
            </Col>
          </Row>

          {isExpanded && (
            <>
              <hr />

              <p>
                <strong>예상 도착 시간:</strong> {route.expectedArrivalTime}
              </p>

              <p>
                <strong>환승 횟수:</strong> {route.transferCount}회
              </p>

              <p>
                <strong>안내:</strong> {route.statusMessage}
              </p>

              <hr />

              <h6>상세 이동 순서</h6>

              {steps.length > 0 ? (
                <ol>
                  {steps.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ol>
              ) : (
                <p className="text-muted">상세 이동 순서가 없습니다.</p>
              )}

              {reasons.length > 0 && (
                <>
                  <h6>계산 이유</h6>

                  <ul>
                    {reasons.map((reason, index) => (
                      <li key={index}>{reason}</li>
                    ))}
                  </ul>
                </>
              )}
            </>
          )}
        </CardBody>
      </Card>
    );
  };

  render() {
    const timeOptions = this.getTimeOptions();
    const {result, loading, theme} = this.state;

    return (
      <>
        <DemoNavbar />

        <main ref="main">
          <section className="section section-shaped section-lg">
            <div
              className="shape shape-style-1"
              style={{
                background:
                  theme === "pink"
                    ? "linear-gradient(150deg,#ffb6c1 15%,#ff8fab 70%,#ff5e8a 94%)"
                    : theme === "purple"
                    ? "linear-gradient(150deg,#c8a2ff 15%,#a66cff 70%,#8b4dff 94%)"
                    : theme === "blue"
                    ? "linear-gradient(150deg,#7795f8 15%,#6772e5 70%,#555abf 94%)"
                    : "linear-gradient(150deg,#172b4d 15%,#1a174d 70%,#22204d 94%)"
              }}
            >
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
                      <div className="position-relative text-center mt-4">
                        <Button
                          onClick={async () => {
                            const lateProbability =
                              result.routes[0].lateProbability;
                            const response = await fetch(
                              `http://127.0.0.1:8000/playlist?late_probability=${lateProbability}`
                            );
                            const data = await response.json();
                            this.setState((prevState) => ({
                              playlists: data.playlist,
                              showPlaylist: !prevState.showPlaylist,
                            }));
                          }}
                          style={{
                            position: "absolute",
                            right: "-100px",
                            top: "-100px",
                            zIndex: "10",
                            width: "70px",
                            height: "70px",
                            borderRadius: "50%",
                            fontSize: "40px",
                            padding: "0",
                            backgroundColor: "transparent",
                            border: "none",
                            boxShadow: "none",
                            outline: "none",
                          }}
                        >
                          🎧
                        </Button>
                      </div>
                      <div className="text-center mt-5"
                        style={{ marginLeft: "-7px" }}>
                        <Button
                          color="warning"
                          size="lg"
                          disabled={this.state.arrivedToday || this.state.arriving}
                          onClick={async () => {
                            const lateProbability =
                              parseInt(result.routes[0].lateProbability);
                            const commuteMinutes =
                              parseInt(result.routes[0].totalMinutes);
                            this.setState({
                              arriving: true,
                            });
                            let data = null;
                              try {
                              const classStartTime =
                                result.classStartTime;
                              const loginId =
                                localStorage.getItem("loginId");
                              const response = await fetch(
                                `http://127.0.0.1:8000/points?login_id=${loginId}&late_probability=${lateProbability}&commute_minutes=${commuteMinutes}&class_start_time=${classStartTime}`
                              );
                              data = await response.json();
                            } catch (error) {
                              console.error(error);
                              this.setState({
                                arriving: false,
                              });
                              return;
                            }
                            this.setState({
                              arriving: false,
                              pointResult: data,
                              arrivedToday: true,
                            });
                          }}
                        >
                          학교 도착!
                        </Button>
                      </div>
                      {this.state.pointResult && (
                        <Card className="mt-4">
                          <CardBody>
                            <h4>
                              🎉 포인트 / 뱃지 획득 결과
                            </h4>
                            <Row className="mt-4">
                              {/* 왼쪽 */}
                              <Col md="6">
                                <h5>
                                  획득 포인트
                                </h5>
                                <ul>
                                  {this.state.pointResult?.point_result?.missions?.map(
                                    (mission, index) => (
                                      <li key={index}>
                                        {mission}
                                      </li>
                                    )
                                  )}
                                </ul>
                                {this.state.pointResult?.point_result?.earned_points > 0 ? (
                                  <p className="mt-3">
                                    +{this.state.pointResult?.point_result?.earned_points}P 획득
                                  </p>
                                ) : (
                                  <p className="mt-3 text-muted">
                                    이번에는 포인트를 얻지 못했어요!
                                  </p>
                                )}
                              </Col>
                              {/* 오른쪽 */}
                              <Col md="6">
                                <h5>
                                  획득 뱃지
                                </h5>
                                {(
                                  this.state.pointResult?.badge_result
                                    ?.earned_badges?.length || 0
                                ) === 0 ? (
                                  <p className="mt-3 text-muted">
                                    이번에는 뱃지를 얻지 못했어요!
                                  </p>
                                ) : (
                                  <ul>

                                  {this.state.pointResult?.badge_result
                                    ?.earned_badges?.includes(
                                      "여유로운 통학의 신"
                                    ) && (
                                    <li>
                                      여유로운 통학의 신{" "}
                                      {this.state.pointResult.badge_result.badge_data.easy_success_count}
                                      / 30
                                    </li>
                                  )}

                                  {this.state.pointResult?.badge_result
                                    ?.earned_badges?.includes(
                                      "아슬아슬 마스터"
                                    ) && (
                                    <li>
                                      아슬아슬 마스터{" "}
                                      {this.state.pointResult.badge_result.badge_data.hard_success_count}
                                      / 10
                                    </li>
                                  )}

                                  {this.state.pointResult?.badge_result
                                    ?.earned_badges?.includes(
                                      "비를 뚫는 자"
                                    ) && (
                                    <li>
                                      비를 뚫는 자{" "}
                                      {this.state.pointResult.badge_result.badge_data.rain_success_count}
                                      / 10
                                    </li>
                                  )}

                                  {this.state.pointResult?.badge_result
                                    ?.earned_badges?.includes(
                                      "새벽 통학생"
                                    ) && (
                                    <li>
                                      새벽 통학생{" "}
                                      {this.state.pointResult.badge_result.badge_data.early_morning_count}
                                      / 20
                                    </li>
                                  )}

                                  {this.state.pointResult?.badge_result
                                    ?.earned_badges?.includes(
                                      "강철 체력"
                                    ) && (
                                    <li>
                                      강철 체력{" "}
                                      {this.state.pointResult.badge_result.badge_data.long_distance_count}
                                      / 20
                                    </li>
                                  )}
                                </ul>
                               )}
                              </Col>
                            </Row>
                          </CardBody>
                        </Card>
                      )}
                      {this.state.showPlaylist && (
                        <Card className="mt-4 text-left">
                          <CardBody>
                            <h4>
                              🎧 추천 플레이리스트
                            </h4>
                            <ul>
                              {this.state.playlists?.map(
                                (playlist, index) => (
                                  <li key={index}>
                                    <a
                                      href={playlist.url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      style={{
                                        color: "black",
                                        textDecoration: "none",
                                      }}
                                    >
                                      {playlist.title}
                                    </a>
                                  </li>
                                )
                              )}
                            </ul>
                          </CardBody>
                        </Card>
                      )}
                      {result.routes.some(
                        (route) => route.lateProbability <= 30
                      ) && (
                        <div className="text-center mt-5">
                          <Button
                            color="success"
                            onClick={() =>
                              window.open(
                                "http://127.0.0.1:8000/game",
                                "_blank"
                              )
                            }
                          >
                            🎮 미니게임
                          </Button>
                          <p className="text-white mt-3 text-center">
                            지각 확률이 낮아 여유 시간이 있어 미니게임이 활성화되었습니다!
                          </p>
                        </div>
                      )}
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