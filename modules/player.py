from .team import Team

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import sys
import traceback
import mysql.connector

class Player(Team):
    def __init__(self):
        super().__init__()
        self.list_player_urls = []
        self.dict_row = {
            "team_url": None,
            "player_url": None,
            "name": None,
            "position": None,
            "info_other": None,
            "rating_overall": None,
            "rating_potential": None,
            "preferred_foot": None,
            "weak_foot": None,
            "skill_moves": None,
            "attacking_work_rate": None,
            "defensive_work_rate": None,
            "player_id": None,
            "specialities": None,
            "crossing": None,
            "finishing": None,
            "heading_accuracy": None,
            "short_passing": None,
            "volleys": None,
            "dribbling": None,
            "curve": None,
            "fk_accuracy": None,
            "long_passing": None,
            "ball_control": None,
            "acceleration": None,
            "sprint_speed": None,
            "agility": None,
            "reactions": None,
            "balance": None,
            "shot_power": None,
            "jumping": None,
            "stamina": None,
            "strength": None,
            "long_shots": None,
            "aggression": None,
            "interceptions": None,
            "positioning": None,
            "vision": None,
            "penalties": None,
            "composure": None,
            "defensive_awareness": None,
            "standing_tackle": None,
            "sliding_tackle": None,
            "gk_diving": None,
            "gk_handling": None,
            "gk_kicking": None,
            "gk_positioning": None,
            "gk_reflexes": None,
            "traits": None
        }
        self.list_dict_row = []
        self.mysql_table = "players_raw"
        self.query_create_table = f"""
        CREATE TABLE IF NOT EXISTS {self.mysql_table} (
            team_url TEXT,
            player_url TEXT,
            name TEXT,
            position TEXT,
            info_other TEXT,
            rating_overall TEXT,
            rating_potential TEXT,
            preferred_foot TEXT,
            weak_foot TEXT,
            skill_moves TEXT,
            attacking_work_rate TEXT,
            defensive_work_rate TEXT,
            player_id VARCHAR(255) PRIMARY KEY,
            specialities TEXT,
            crossing TEXT,
            finishing TEXT,
            heading_accuracy TEXT,
            short_passing TEXT,
            volleys TEXT,
            dribbling TEXT,
            curve TEXT,
            fk_accuracy TEXT,
            long_passing TEXT,
            ball_control TEXT,
            acceleration TEXT,
            sprint_speed TEXT,
            agility TEXT,
            reactions TEXT,
            balance TEXT,
            shot_power TEXT,
            jumping TEXT,
            stamina TEXT,
            strength TEXT,
            long_shots TEXT,
            aggression TEXT,
            interceptions TEXT,
            positioning TEXT,
            vision TEXT,
            penalties TEXT,
            composure TEXT,
            defensive_awareness TEXT,
            standing_tackle TEXT,
            sliding_tackle TEXT,
            gk_diving TEXT,
            gk_handling TEXT,
            gk_kicking TEXT,
            gk_positioning TEXT,
            gk_reflexes TEXT,
            traits TEXT
        );
        """
        try:
            self.connection, self.cursor = self.connect_to_mysql()
            print("Connected to MySQL!")
        except Exception as e:
            print(e)
        try:
            self.run_mysql_query(self.query_create_table)
        except Exception as e:
            print(e)

    def __enter__(self):
        pass

    def __exit__(self):
        self.close_mysql_connection(self.connection)
        return

    def connect_to_mysql(self):
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="12345",
            database="fifa"
        )
        return(connection, connection.cursor())
    
    def run_mysql_query(self, query):
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            self.connection.commit()
            return(rows)
        except Exception as e:
            print(e)
            return(False)

    def close_mysql_connection(self, connection):
        try:
            connection.close()
            return(True)
        except Exception as e:
            print(e)
            return(False)

    def fetch_player_urls(self, list_team_urls):
        for team_url in tqdm(list_team_urls):
            soup = BeautifulSoup(requests.get(team_url).content, "html.parser")
            table = soup.find("table", {"class":"table table-hover persist-area"})
            table_body = table.find("tbody")
            rows = table_body.find_all("tr")
            for row in rows:
                a_class = row.find("td", {"class": "col-name"}).find("a")
                href = a_class["href"]
                player_url = "https://sofifa.com" + href
                # self.list_player_urls.append([team_url, player_url])
                self.list_dict_row.append(self.combine_player_info(BeautifulSoup(requests.get(player_url).content, "html.parser"), team_url, player_url))
        return
    
    def combine_player_info(self, soup, team_url, player_url):
        try:
            name, position, info_other, rating_overall, rating_potential, preferred_foot, weak_foot, skill_moves, attacking_work_rate, defensive_work_rate, player_id, specialities = self.get_player_info_1(soup)
            crossing, finishing, heading_accuracy, short_passing, volleys = self.get_player_info_2(soup)
            dribbling, curve, fk_accuracy, long_passing, ball_control = self.get_player_info_3(soup)
            acceleration, sprint_speed, agility, reactions, balance = self.get_player_info_4(soup)
            shot_power, jumping, stamina, strength, long_shots = self.get_player_info_5(soup)
            aggression, interceptions, positioning, vision, penalties, composure = self.get_player_info_6(soup)
            defensive_awareness, standing_tackle, sliding_tackle = self.get_player_info_7(soup)
            gk_diving, gk_handling, gk_kicking, gk_positioning, gk_reflexes, traits = self.get_player_info_8(soup)
            dict_row = {
                "team_url": team_url,
                "player_url": player_url,
                "name": name,
                "position": position,
                "info_other": info_other,
                "rating_overall": rating_overall,
                "rating_potential": rating_potential,
                "preferred_foot": preferred_foot,
                "weak_foot": weak_foot,
                "skill_moves": skill_moves,
                "attacking_work_rate": attacking_work_rate,
                "defensive_work_rate": defensive_work_rate,
                "player_id": player_id,
                "specialities": specialities,
                "crossing": crossing,
                "finishing": finishing,
                "heading_accuracy": heading_accuracy,
                "short_passing": short_passing,
                "volleys": volleys,
                "dribbling": dribbling,
                "curve": curve,
                "fk_accuracy": fk_accuracy,
                "long_passing": long_passing,
                "ball_control": ball_control,
                "acceleration": acceleration,
                "sprint_speed": sprint_speed,
                "agility": agility,
                "reactions": reactions,
                "balance": balance,
                "shot_power": shot_power,
                "jumping": jumping,
                "stamina": stamina,
                "strength": strength,
                "long_shots": long_shots,
                "aggression": aggression,
                "interceptions": interceptions,
                "positioning": positioning,
                "vision": vision,
                "penalties": penalties,
                "composure": composure,
                "defensive_awareness": defensive_awareness,
                "standing_tackle": standing_tackle,
                "sliding_tackle": sliding_tackle,
                "gk_diving": gk_diving,
                "gk_handling": gk_handling,
                "gk_kicking": gk_kicking,
                "gk_positioning": gk_positioning,
                "gk_reflexes": gk_reflexes,
                "traits": traits
            }
            # self.list_dict_row.append(dict_row)
        
            # Inserting into the MySQL table

            columns = ", ".join(list(dict_row.keys()))
            values = ", ".join([f'"{item}"' for item in list(dict_row.values())])
            query = f"INSERT IGNORE INTO {self.mysql_table} ({columns}) VALUES ({values})"
            self.run_mysql_query(query)
        except Exception as e:
            traceback.print_exc()
            print(team_url, player_url)
            print(e)
            sys.exit(1)
        return(dict_row)

    def get_player_info_1(self, soup):
        dict_row = self.dict_row
        dict_row["name"] = soup.select("h1")[1].findAll(text=True)[0]
        # position = soup.find("span", {"class": "pos pos0"}).findAll(text=True)[0]
        dict_row["position"] = soup.find("div", {"class": "meta bp3-text-overflow-ellipsis"}).findAll(text=True)[1].strip()
        # try:
        #     dict_row["info_other"] = soup.find("div", {"class": "meta bp3-text-overflow-ellipsis"}).findAll(text=True)[2].strip()
        # except Exception:
        #     pass
        dict_row["info_other"] = None
        dict_row["rating_overall"] = soup.find_all("div", {"class": "column col-3"})[0].findAll(text=True)[0].strip()
        dict_row["rating_potential"] = soup.find_all("div", {"class": "column col-3"})[1].findAll(text=True)[0].strip()
        for li in soup.find_all("ul", {"class": "pl"})[0].findAll("li"):
            l = li.findAll(text=True)
            if("Preferred Foot" in l[0]):
                dict_row["preferred_foot"] = l[1].strip()
            if("Weak Foot" in l[-1]):
                dict_row["weak_foot"] = l[0].strip()
            if("Skill Moves" in l[-1]):
                dict_row["skill_moves"] = l[0].strip()
            if("Work Rate" in l[0]):
                dict_row["attacking_work_rate"] = l[-1].split("/")[0].strip()
                dict_row["defensive_work_rate"] = l[-1].split("/")[1].strip()
            if("ID" in l[0]):
                dict_row["player_id"] = l[-1].strip()
        dict_row["specialities"] = ", ".join([li.findAll(text=True)[0].split("#")[-1] for li in soup.find_all("ul", {"class": "pl"})[1].findAll("li")])

        return(dict_row["name"], dict_row["position"], dict_row["info_other"], dict_row["rating_overall"], dict_row["rating_potential"], dict_row["preferred_foot"], dict_row["weak_foot"], dict_row["skill_moves"], dict_row["attacking_work_rate"], dict_row["defensive_work_rate"], dict_row["player_id"], dict_row["specialities"])

    def get_player_info_2(self, soup):
        dict_row = self.dict_row
        for li in soup.find_all("div", {"class": "card"})[3].findAll("li"):
            li = li.findAll(text=True)
            li = [item for item in li if(not all(char in [" ", "\n"] for char in item))]
            if("Crossing" in li):
                dict_row["crossing"] = li[0]
            if("Finishing" in li):
                dict_row["finishing"] = li[0]
            if("Heading Accuracy" in li):
                dict_row["heading_accuracy"] = li[0]
            if("Short Passing" in li):
                dict_row["short_passing"] = li[0]
            if("Volleys" in li):
                dict_row["volleys"] = li[0]
        return(dict_row["crossing"], dict_row["finishing"], dict_row["heading_accuracy"], dict_row["short_passing"], dict_row["volleys"])

    def get_player_info_3(self, soup):
        dict_row = self.dict_row
        for li in soup.find_all("div", {"class": "card"})[4].findAll("li"):
            li = li.findAll(text=True)
            li = [item for item in li if(not all(char in [" ", "\n"] for char in item))]
            if("Dribbling" in li):
                dict_row["dribbling"] = li[0]
            if("Curve" in li):
                dict_row["curve"] = li[0]
            if("FK Accuracy" in li):
                dict_row["fk_accuracy"] = li[0]
            if("Long Passing" in li):
                dict_row["long_passing"] = li[0]
            if("Ball Control" in li):
                dict_row["ball_control"] = li[0]
        return(dict_row["dribbling"], dict_row["curve"], dict_row["fk_accuracy"], dict_row["long_passing"], dict_row["ball_control"])

    def get_player_info_4(self, soup):
        dict_row = self.dict_row
        for li in soup.find_all("div", {"class": "card"})[5].findAll("li"):
            li = li.findAll(text=True)
            li = [item for item in li if(not all(char in [" ", "\n"] for char in item))]
            if("Acceleration" in li):
                dict_row["acceleration"] = li[0]
            if("Sprint Speed" in li):
                dict_row["sprint_speed"] = li[0]
            if("Agility" in li):
                dict_row["agility"] = li[0]
            if("Reactions" in li):
                dict_row["reactions"] = li[0]
            if("Balance" in li):
                dict_row["balance"] = li[0]
        return(dict_row["acceleration"], dict_row["sprint_speed"], dict_row["agility"], dict_row["reactions"], dict_row["balance"])

    def get_player_info_5(self, soup):
        dict_row = self.dict_row
        for li in soup.find_all("div", {"class": "card"})[6].findAll("li"):
            li = li.findAll(text=True)
            li = [item for item in li if(not all(char in [" ", "\n"] for char in item))]
            if("Shot Power" in li):
                dict_row["shot_power"] = li[0]
            if("Jumping" in li):
                dict_row["jumping"] = li[0]
            if("Stamina" in li):
                dict_row["stamina"] = li[0]
            if("Strength" in li):
                dict_row["strength"] = li[0]
            if("Long Shots" in li):
                dict_row["long_shots"] = li[0]
        return(dict_row["shot_power"], dict_row["jumping"], dict_row["stamina"], dict_row["strength"], dict_row["long_shots"])

    def get_player_info_6(self, soup):
        dict_row = self.dict_row
        for li in soup.find_all("div", {"class": "card"})[7].findAll("li"):
            li = li.findAll(text=True)
            li = [item for item in li if(not all(char in [" ", "\n"] for char in item))]
            li = [item.strip() for item in li]
            if("Aggression" in li):
                dict_row["aggression"] = li[0]
            if("Interceptions" in li):
                dict_row["interceptions"] = li[0]
            if("Positioning" in li):
                dict_row["positioning"] = li[0]
            if("Vision" in li):
                dict_row["vision"] = li[0]
            if("Penalties" in li):
                dict_row["penalties"] = li[0]
            if("Composure" in li):
                dict_row["composure"] = li[0]
        return(dict_row["aggression"], dict_row["interceptions"], dict_row["positioning"], dict_row["vision"], dict_row["penalties"], dict_row["composure"])

    def get_player_info_7(self, soup):
        dict_row = self.dict_row
        for li in soup.find_all("div", {"class": "card"})[8].findAll("li"):
            li = li.findAll(text=True)
            li = [item for item in li if(not all(char in [" ", "\n"] for char in item))]
            li = [item.strip() for item in li]
            if("Defensive Awareness" in li):
                dict_row["defensive_awareness"] = li[0]
            if("Standing Tackle" in li):
                dict_row["standing_tackle"] = li[0]
            if("Sliding Tackle" in li):
                dict_row["sliding_tackle"] = li[0]
        return(dict_row["defensive_awareness"], dict_row["standing_tackle"], dict_row["sliding_tackle"])

    def get_player_info_8(self, soup):
        dict_row = self.dict_row
        for li in soup.find_all("div", {"class": "card"})[9].findAll("li"):
            li = li.findAll(text=True)
            li = [item for item in li if(not all(char in [" ", "\n"] for char in item))]
            li = [item.strip() for item in li]
            if("GK Diving" in li):
                dict_row["gk_diving"] = li[0]
            if("GK Handling" in li):
                dict_row["gk_handling"] = li[0]
            if("GK Kicking" in li):
                dict_row["gk_kicking"] = li[0]
            if("GK Positioning" in li):
                dict_row["gk_positioning"] = li[0]
            if("GK Reflexes" in li):
                dict_row["gk_reflexes"] = li[0]
        dict_row["traits"] = ", ".join([li.findAll(text=True)[0] for li in soup.find_all("div", {"class": "card"})[11].findAll("li")])
        return(dict_row["gk_diving"], dict_row["gk_handling"], dict_row["gk_kicking"], dict_row["gk_positioning"], dict_row["gk_reflexes"], dict_row["traits"])
    