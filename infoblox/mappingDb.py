"""
A generic mapping object that allows getters and setters and ties classes
back to Infoblox objects.
"""
import logging
from mapping import Mapping

LOGGER = logging.getLogger(__name__)

class MappingDb(Mapping):
    """A generic data object that utilised the Mapping object for JSON related stuff.
    This is used to keep state of the object and sinc with the Infoblox Database

    """

    def __init__(self, session, reference_id=None, **kwargs):
        """Create a new instance of the MappingDB object.

        """
        super(MappingDb, self).__init__(**kwargs)
        self._session = session
        self._ref = reference_id
        self._search_values = self._build_search_values(kwargs)
        if self._ref or self._search_values:
            self.fetch()



    def _assign(self, values):
        """Assign the values passed as either a dict or list to the object if
        the key for each value matches an available attribute on the object.

        :param dict values: The values to assign

        """
        LOGGER.debug('Assigning values: %r', values)
        if not values:
            return
        keys = self.keys()
        if not self._ref:
            keys.append('_ref')
        if isinstance(values, dict):
            for key in keys:
                if values.get(key):
                    if isinstance(values.get(key), list):
                        items = list()
                        for item in values[key]:
                            if isinstance(item, dict):
                                if '_ref' in item:
                                    obj_class = get_class(item['_ref'])
                                    if obj_class:
                                        items.append(obj_class(self._session,
                                                               **item))
                            else:
                                items.append(item)
                        setattr(self, key, items)
                    else:
                        setattr(self, key, values[key])
        elif isinstance(values, list):
            self._assign(values[0])
        else:
            LOGGER.critical('Unhandled return type: %r', values)

    def _build_search_values(self, kwargs):
        """Build the search criteria dictionary. It will first try and build
        the values from already set attributes on the object, falling back
        to the passed in kwargs.

        :param dict kwargs: Values to build the dict from
        :rtype: dict

        """
        criteria = {}
        for key in self._search_by:
            if getattr(self, key, None):
                criteria[key] = getattr(self, key)
            elif key in kwargs and kwargs.get(key):
                criteria[key] = kwargs.get(key)
        return criteria

    @property
    def _path(self):
        return self._ref if self._ref else self._wapi_type

    @property
    def _return_fields(self):
        return ','.join([key for key in self.keys()
                         if key not in self._return_ignore])

    def delete(self):
        """Remove the item from the infoblox server.

        :rtype: bool
        :raises: AssertionError
        :raises: ValueError
        :raises: infoblox.exceptions.ProtocolError

        """
        if not self._ref:
            raise ValueError('Object has no reference id for deletion')
        if 'save' not in self._supports:
            raise AssertionError('Can not save this object type')
        response = self._session.delete(self._path)
        if response.status_code == 200:
            self._ref = None
            self.clear()
            return True
        try:
            error = response.json()
            raise exceptions.ProtocolError(error['text'])
        except ValueError:
            raise exceptions.ProtocolError(response.content)

        
    def fetch(self):
        """Attempt to fetch the object from the Infoblox device. If successful
        the object will be updated and the method will return True.

        :rtype: bool
        :raises: infoblox.exceptions.ProtocolError

        """
        from pudb import set_trace; set_trace()
        
        self._search_values = self._build_search_values({})
        
        LOGGER.debug('Fetching %s, %s', self._path, self._search_values)
        response = self._session.get(self._path, self._search_values,
                                     {'_return_fields': self._return_fields})
        if response.status_code == 200:
            values = response.json()
            self._assign(values)
            return bool(values)
        elif response.status_code >= 400:
            try:
                error = response.json()
                raise exceptions.ProtocolError(error['text'])
            except ValueError:
                raise exceptions.ProtocolError(response.content)
        return False

    def reference_id(self):
        """Return a read-only handle for the reference_id of this object.

        """
        return str(self._ref)
    
    def save(self):
        """Update the infoblox with new values for the specified object, or add
        the values if it's a new object all together.

        :raises: AssertionError
        :raises: infoblox.exceptions.ProtocolError

        """
        from pudb import set_trace; set_trace()
        
        
        if 'save' not in self._supports:
            raise AssertionError('Can not save this object type')

        values = {}
        for key in [key for key in self.keys() if key not in self._save_ignore]:
            if not getattr(self, key) and getattr(self, key) != False:
                continue

            if isinstance(getattr(self, key, None), list):
                value = list()
                for item in getattr(self, key):
                    if isinstance(item, dict):
                        value.append(item)
                    elif hasattr(item, '_save_as'):
                        value.append(item._save_as())
                    elif hasattr(item, '_ref') and getattr(item, '_ref'):
                        value.append(getattr(item, '_ref'))
                    else:
                        LOGGER.warning('Cant assign %r', item)
                values[key] = value
            elif getattr(self, key, None):
                values[key] = getattr(self, key)
        if not self._ref:
            response = self._session.post(self._path, values)
        else:
            values['_ref'] = self._ref
            response = self._session.put(self._path, values)
        LOGGER.debug('Response: %r, %r', response.status_code, response.content)
        if 200 <= response.status_code <= 201:
            self.fetch()
            return True
        else:
            try:
                error = response.json()
                raise exceptions.ProtocolError(error['text'])
            except ValueError:
                raise exceptions.ProtocolError(response.content)




 

