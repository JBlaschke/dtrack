from textwrap    import dedent
from collections import namedtuple


class DBTransactionAdapter(object):

    def __init__(self, db_connection):
        self._con = db_connection
        self.QResult = namedtuple(
            "QResult", 
            (
                "idx", "t", "rank", "slurm_job_id", "slurm_node_list",
                "function_name", "file_path", "file_offset"
            ),
            defaults = (-1, 0., 0, "", "", "", "", 0)
        )


    def last_entry(self):
        r = self._con.execute(
            dedent(
                f"""\
                SELECT * FROM {self._con.table}
                    ORDER BY idx DESC LIMIT 1
                """
            ).rstrip()
        )

        if r > 0:
            return self.QResult(*self._con.result)
        return self.QResult(-1)


    def get_entry(self, idx):
        r = self._con.execute(
            dedent(
                f"""\
                SELECT * FROM {self._con.table} WHERE idx={idx}
                """
            ).rstrip()
        )

        if r > 0:
            return self.QResult(*self._con.result)
        return self.QResult(-1)

    def new_entry(
            self,
            t, rank,
            slurm_job_id, slurm_node_list,
            function_name,
            file_path, file_offset
        ):

        sql_cmd = dedent(
            """\
            BEGIN;
            """
        )
        sql_cmd += dedent(
            f"""\
            INSERT INTO {self._con.table} (
                    t, rank,
                    slurm_job_id, slurm_node_list,
                    flunction_name,
                    file_path, file_offset
                ) VALUES (
                    {t}, {rank},
                    {slurm_job_id}, {slurm_node_list},
                    {function_name},
                    {file_path}, {file_offset}
                );
            """
        )
        sql_cmd += dedent(
            """\
            COMMIT;
            """
        ).rstrip()

        self._con.execute(sql_cmd)
        # no need to commit as `sql_cmd` ends with `COMMIT`
        # self._con.commit()